from sqlalchemy.orm import Session
from sqlalchemy import text
from ..schemas import akun as akun_schemas
from ..models import akun as akun_models

async def get_akun(db: Session, id: int):
    res = db.query(akun_models.Akun).filter(akun_models.Akun.id == id).first()
    return res

async def match_akun(request_in: akun_schemas.MatchAkunIn, db: Session):
    if request_in.mode == "insert":
        ts_queries = [''.join((request_in_data.akun,
                            request_in_data.kelompok,
                            request_in_data.jenis,
                            request_in_data.objek,
                            request_in_data.rincian_objek,
                            request_in_data.sub_rincian_objek,
                            request_in_data.level1,
                            request_in_data.level2,
                            request_in_data.level3,
                            request_in_data.level4,
                            request_in_data.level5,
                            request_in_data.level6)) for request_in_data in request_in.data]
    else:
        ts_queries = [''.join((request_in_data.after.akun,
                    request_in_data.after.kelompok,
                    request_in_data.after.jenis,
                    request_in_data.after.objek,
                    request_in_data.after.rincian_objek,
                    request_in_data.after.sub_rincian_objek,
                    request_in_data.after.level1,
                    request_in_data.after.level2,
                    request_in_data.after.level3,
                    request_in_data.after.level4,
                    request_in_data.after.level5,
                    request_in_data.after.level6)) for request_in_data in request_in.data]

    res = [db.query(akun_models.Akun).filter(
        text(f"""to_tsvector('simple', f_concat_ws('', akun, kelompok, jenis, objek,
                                                    rincian_objek, sub_rincian_objek, 
                                                    level1,level2,level3,
                                                    level4,level5,level6)
             )
             @@ plainto_tsquery('simple', '{ts_query}')""")
    ).first() for ts_query in ts_queries]
    return res


# def get_program(db: Session, id: int):
#     return db.query(models.Program).filter(models.Program.id == id).first()
