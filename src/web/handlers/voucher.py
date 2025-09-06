from typing import List
from pydantic import BaseModel
from config import Config
from voucher.db import Voucher
from voucher.helper import parse_vouchers_file
from voucher.models import Duration, VoucherDB
from fastapi import APIRouter, HTTPException, UploadFile, status


class VoucherCreate(BaseModel):
    code: str
    duration: Duration
    used: bool | None = False


# class VoucherResponse(BaseModel):
#     duration: Duration
#     code: str
#     used: bool


def create_voucher_router(config: Config):
    router = APIRouter()

    @router.get("/vouchers")
    def get_vouchers(
        includeUsed: bool | None = False, duration: Duration | None = None
    ) -> List[Voucher]:
        used = None
        if not includeUsed:
            used = False

        voucherDB = VoucherDB(config)
        vouchers = voucherDB.get_vouchers(duration=duration, used=used)

        if len(vouchers) == 0:
            return []

        return vouchers

    @router.post("/vouchers")
    def add_voucher(voucher_create: VoucherCreate) -> Voucher:
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

    @router.post("/vouchers/upload-file")
    def add_vouchers_file(file: UploadFile) -> dict:
        voucherDB = VoucherDB(config)
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
    def use_voucher(voucher_code: str) -> None:
        voucherDB = VoucherDB(config)
        try:
            voucherDB.use_voucher(voucher_code)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Voucher could not be updated: {e}",
            )

    @router.delete("/vouchers/{voucher_code}")
    def delete_voucher(voucher_code: str) -> None:
        voucherDB = VoucherDB(config)
        try:
            voucherDB.delete_voucher(voucher_code)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Voucher could not be deleted: {e}",
            )

    return router
