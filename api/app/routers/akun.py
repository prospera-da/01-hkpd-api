from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_db
# from .. import crud, models, schemas
from sqlalchemy.orm import Session
from ..controllers import akun as akun_controllers
from ..schemas import akun as akun_schemas

router = APIRouter()

@router.get("/akun/{id}", response_model=akun_schemas.Akun)
async def get_akun(id: int, db: Session = Depends(get_db)):
    akun_record = await akun_controllers.get_akun(db, id=id)

    if akun_record is None:
        raise HTTPException(status_code=404, detail="Akun not found")
    return akun_record

@router.post("/match_akun")
# @router.post("/match_akun", response_model=akun_schemas.MatchAkunOut)
async def match_akun(request_in: akun_schemas.MatchAkunIn, db: Session = Depends(get_db)):
    match_result = await akun_controllers.match_akun(request_in=request_in, db=db)
    if match_result is None:
        raise HTTPException(status_code=404, detail="Akun not found")
    return match_result