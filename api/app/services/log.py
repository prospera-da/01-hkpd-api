from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models import log as log_models
from ..schemas import akun as akun_schemas
from typing import Dict, List, Union
from hashlib import sha256
from datetime import datetime

async def insert_log(log: Dict, db: Session):
    data_string = [''.join(i) for i in [dict(data).values() for data in log["data"]]]
    data_hash = [sha256(data.encode("utf-8")).hexdigest() for data in data_string]
    match_with_ground_truth = [True if data else False for data in log["match_result"]]
    ground_truth_id = [data.id if data else None for data in log["match_result"]]
    ids = []
    for idx,data in enumerate(log["data"]):

        record = log_models.Log(data = str(dict(data)),
                                data_hash = data_hash[idx],
            match_with_ground_truth = match_with_ground_truth[idx],
            ground_truth_id = ground_truth_id[idx],
            created_at = datetime.now(),
        )
        db.add(record)
        db.commit()
        ids.append(record.id)
    print("Log has been added")
    return ids

async def search_log(request_in: akun_schemas.MatchAkunIn, db: Session):
    data_string = [''.join(i) for i in [dict(data.before).values() for data in request_in.data]]
    data_hash = [sha256(data.encode("utf-8")).hexdigest() for data in data_string]

    res = [db.query(log_models.Log).filter_by(
                data_hash=hash,
                match_with_ground_truth=False
            ).first() for hash in data_hash]
    return res

async def update_log(logs: List[Union[log_models.Log,None]], inserted_log_id:List[int], db: Session):
    for idx, log_data in enumerate(logs):
        if log_data:
            db.query(log_models.Log).\
                filter_by(id = log_data.id).\
                update({'updated_by': inserted_log_id[idx],'updated_at':datetime.now()})
            db.commit()
    print("Data has been updated")