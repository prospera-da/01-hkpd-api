from pydantic import BaseModel
from enum import Enum
from typing import Union, Optional, List

class ModeEnum(str, Enum):
    insert = 'insert'
    update = 'update'

class BaseAkun(BaseModel):
    akun: str
    kelompok: str
    jenis: str
    objek: str
    rincian_objek: str
    sub_rincian_objek: str
    level1: str
    level2: str
    level3: str
    level4: str
    level5: str
    level6: str

    class Config:
        orm_mode = True

class Akun(BaseModel):
    id: int
    akun: str
    kelompok: str
    jenis: str
    objek: str
    rincian_objek: str
    sub_rincian_objek: str
    level1: str
    level2: str
    level3: str
    level4: str
    level5: str
    level6: str

    class Config:
        orm_mode = True

class UpdateAkun(BaseModel):
    before: BaseAkun
    after: BaseAkun

class MatchAkunIn(BaseModel):
    province: str
    regency: str
    district: str
    mode: ModeEnum
    data: List[Union[BaseAkun, UpdateAkun]]

    class Config:
        orm_mode = True

class MatchResponse(BaseModel):
    total_records: int
    matches_found: int
    mismatched_records_count: int
    mismatched_records: List[BaseAkun]

class MatchAkunOut(BaseModel):
    status: str
    time_elapsed: int
    data: MatchResponse

class AkunIn(BaseModel):
    id: int
    akun: str
    kelompok: str
    jenis: str
    objek: str
    rincian_objek: str
    sub_rincian_objek: str
    level1: str
    level2: str
    level3: str
    level4: str
    level5: str
    level6: str

    class Config:
        orm_mode = True

class Program(BaseModel):
    id : int
    jenis_pemda: str
    kode_fungsi: str
    fungsi: str
    kode_sub_fungsi: str
    sub_fungsi: str
    kode_urusan: str
    urusan_unsur: str
    kode_bidang: str
    uraian_bidang: str
    kode_program: str
    uraian_program: str
    kode_kegiatan: str
    uraian_kegiatan: str
    kode_sub_kegiatan: str
    uraian_sub_kegiatan: str
    kinerja: str
    indikator: str
    satuan: str

    class Config:
        orm_mode = True
