from typing import List
from pydantic import BaseModel
from user.auth import validate_jwt_token
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from config import Config
from db.models import Voucher
from voucher.helper import parse_vouchers_file
from voucher.models import Duration, VoucherDB
from fastapi import APIRouter, HTTPException, Request, UploadFile, status


class VoucherCreate(BaseModel):
    code: str
    duration: Duration
    used: bool | None = False


def auth_user(request: Request, config: Config) -> str:
    token = request.cookies.get("authToken")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auth token missing",
        )

    try:
        auth_user = validate_jwt_token(token, config.secret_key)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Issue with JWT Token: {e}",
        )

    return auth_user


def create_voucher_router(config: Config):
    router = APIRouter()

    @router.get("/vouchers")
    def get_vouchers(
        request: Request,
        includeUsed: bool | None = False,
        duration: Duration | None = None,
    ) -> List[Voucher]:
        _ = auth_user(request, config)

        used = None
        if not includeUsed:
            used = False

        voucherDB = VoucherDB(config)
        vouchers = voucherDB.get_vouchers(duration=duration, used=used)

        if len(vouchers) == 0:
            return []

        return vouchers

    @router.post("/vouchers", status_code=HTTP_201_CREATED)
    def add_voucher(request: Request, voucher_create: VoucherCreate) -> Voucher:
        _ = auth_user(request, config)

        voucherDB = VoucherDB(config)
        try:
            added_voucher = voucherDB.add_voucher(
                voucher_create.code, voucher_create.duration
            )
        except (ValueError, KeyError) as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Voucher could not be entered: {e}",
            )

        return added_voucher

    @router.post("/vouchers/upload-file", status_code=HTTP_201_CREATED)
    async def add_vouchers_file(file: UploadFile) -> dict:
        # _ = auth_user(request, config)
        voucherDB = VoucherDB(config)
        print("add_vouchers_file", file)
        file_contents = file.file.read()

        if file.filename is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File type not clear"
            )

        try:
            vouchers_input = parse_vouchers_file(file.filename, file_contents)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Data could not be parsed: {e}",
            )

        created_vouchers = []
        failed_vouchers = []

        for code, duration in vouchers_input:
            try:
                new_voucher = voucherDB.add_voucher(code, duration)
                created_vouchers.append(new_voucher)
            except Exception as e:
                failed_vouchers.append({"code": code, "error": str(e)})

        return {
            "created_vouchers": created_vouchers,
            "created_count": len(created_vouchers),
            "failed_vouchers": failed_vouchers,
            "failed_count": len(failed_vouchers),
        }

    @router.put("/vouchers/{voucher_code}")
    def use_voucher(request: Request, voucher_code: str) -> None:
        _ = auth_user(request, config)
        voucherDB = VoucherDB(config)
        try:
            voucherDB.use_voucher(voucher_code)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Voucher could not be updated: {e}",
            )

    @router.delete("/vouchers/{voucher_code}", status_code=HTTP_204_NO_CONTENT)
    def delete_voucher(request: Request, voucher_code: str) -> None:
        _ = auth_user(request, config)
        voucherDB = VoucherDB(config)
        try:
            voucherDB.delete_voucher(voucher_code)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Voucher could not be deleted: {e}",
            )

    return router
