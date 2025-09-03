from typing import List
from pydantic import BaseModel
from config import Config
from voucher.db import Voucher
from voucher.models import Duration, VoucherDB
from fastapi import APIRouter, HTTPException, status


class VoucherCreate(BaseModel):
    duration: Duration
    code: str
    used: bool | None = False


class VoucherResponse(BaseModel):
    duration: Duration
    code: str
    used: bool


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
