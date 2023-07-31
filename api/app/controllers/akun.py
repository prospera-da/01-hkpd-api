from ..schemas import akun as akun_schemas
from ..services import akun as akun_services
from ..services import log as log_services
from sqlalchemy.orm import Session
from fastapi import HTTPException
import time


DATE_LIST = ["partition_date"]
TIMESTAMP_LIST = ["timestamp"]
BOOLEAN_LIST = ["is_legit"]


async def get_akun(db: Session, id:int):
    # get akun based on id
    akun_record = await akun_services.get_akun(db, id)
    if akun_record is None:
        raise HTTPException(status_code=404, detail="Akun not found")
    return akun_record


async def match_akun(request_in: akun_schemas.MatchAkunIn, db: Session):
    start_time = time.time()
    sub_response = {"total_records": len(request_in.data),
                    "mismatched_records":request_in.data}
    response = {}
    # insert logic
    if request_in.mode=='insert':
        match_result = await akun_services.match_akun(request_in, db)        

        if match_result:
            # update sub_response
            number_of_mismatched_records = match_result.count(None)
            mismatched_indices = [i for i,v in enumerate(match_result) if v==None]
            mismatched_records = [request_in.data[i] for i in mismatched_indices]
            sub_response.update({"matches_found":len(match_result) - number_of_mismatched_records,
                                "mismatched_records_count":number_of_mismatched_records,
                                "mismatched_records":mismatched_records})
            # craft response
            response.update({"status":"SUCCESS",
                            "data":sub_response})
            
            # insert to log table
            await log_services.insert_log(log={"data":request_in.data,
                                               "match_result":match_result},
                                               db=db)
        else:
            raise HTTPException(status_code=404, detail="Akun not found")
    elif request_in.mode == "update":
        # search_log
        log_search_res = await log_services.search_log(request_in=request_in,db=db)
        
        # match after
        match_result = await akun_services.match_akun(request_in, db) 

        # insert eligible log
        eligible_data = [data.after for i, data in enumerate(request_in.data) if log_search_res[i]!=None]
        eligible_match_result = [data for i, data in enumerate(match_result) if log_search_res[i]!=None]
        inserted_log_ids = await log_services.insert_log(log={"data":eligible_data,
                                            "match_result":eligible_match_result},
                                            db=db)

        # update old record
        await log_services.update_log(log_search_res,inserted_log_ids,db)

        # update sub_response
        number_of_mismatched_records = eligible_match_result.count(None)
        mismatched_indices = [i for i,v in enumerate(eligible_match_result) if v==None]
        mismatched_records = [request_in.data[i] for i in mismatched_indices]
        sub_response.update({"matches_found":len(eligible_match_result) - number_of_mismatched_records,
                            "mismatched_records_count":number_of_mismatched_records,
                            "mismatched_records":mismatched_records})
        # craft response
        response.update({"status":"SUCCESS",
                        "data":sub_response})


    elapsed_time = time.time() - start_time
    response.update({"time_elapsed":elapsed_time})
    return response