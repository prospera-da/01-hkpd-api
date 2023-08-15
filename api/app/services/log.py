from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models import log as log_models
from ..schemas import akun as akun_schemas
from typing import Dict, List, Union
from hashlib import sha256
from datetime import datetime

async def insert_log(log: Dict, updated_parent_id: List[int], db: Session):
    joined_values=[]
    for i in [dict(data)  for data in log["data"] ]:
       for key,value in i.items():

           if key!='id':
              joined_values.append(value)
  
    data_string=''.join(joined_values)
    data_hash = [sha256(data.encode("utf-8")).hexdigest() for data in data_string]
    match_with_ground_truth = [True if data else False for data in log["match_result"]]
    ground_truth_id = [data.id if data else None for data in log["match_result"]]

    #parent_log_id=[data if data!=None else None for data in updated_parent_id]

    
    ids = []
    for idx,data in enumerate(log["data"]):
        dict_data= {key:value for key, value in dict(data).items() if key!='id'}

        record = log_models.Log(data = str(dict_data),
                                data_hash = data_hash[idx],
            match_with_ground_truth = match_with_ground_truth[idx],
            ground_truth_id = ground_truth_id[idx],
            updated_parent_id=updated_parent_id[idx],
            created_at = datetime.now(),
        )
        db.add(record)
        db.commit()
        ids.append(record.id)
    print("Log has been added")
    return ids

async def search_log(request_in: akun_schemas.MatchAkunIn, db: Session):
    #data_string = [i if dict(data).keys()=='id' else 0 for i in [dict(data).values() for data in request_in.data]]
    #data_hash = [sha256(data.encode("utf-8")).hexdigest() for data in data_string]
    log_id=[int(item) for item in [''.join (str(request_in_data.id)) for request_in_data in request_in.data]]

    res = (db.query(log_models.Log).filter(log_models.Log.id.in_(log_id)).all() )
    sorted_logs = sorted(res, key=lambda log: log_id.index(log.id))
    return sorted_logs

async def update_log(logs: List[Union[log_models.Log,None]], inserted_log_id:List[int], db: Session):
    for idx, log_data in enumerate(logs):
        if log_data:
            db.query(log_models.Log).\
                filter_by(id = log_data.id).\
                update({'updated_by': inserted_log_id[idx],'updated_at':datetime.now()})
            db.commit()
    print("Data has been updated")