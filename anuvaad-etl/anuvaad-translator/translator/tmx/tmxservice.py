import hashlib
import json
import time

import uuid
import xlrd
from anuvaad_auditor.loghandler import log_exception, log_info
import requests
from .tmxrepo import TMXRepository
from configs.translatorconfig import nmt_labse_align_url, download_folder, tmx_global_enabled, tmx_org_enabled, \
    tmx_user_enabled, tmx_word_length
from anuvaad_auditor.errorhandler import post_error

repo = TMXRepository()


class TMXService:

    def __init__(self):
        pass

    # Read a CSV and creates TMX entries.
    def push_csv_to_tmx_store(self, api_input):
        log_info("Bulk Create....", None)
        try:
            if 'context' not in api_input.keys() or 'filePath' not in api_input.keys():
                return {"message": "context and filePath are mandatory", "status": "FAILED"}
            extension = str(api_input["filePath"]).split(".")[1]
            if extension not in ["xls", "xlsx"]:
                return {"message": "Invalid file, TMX only supports - xls & xlsx", "status": "FAILED"}
            file_path = download_folder + api_input["filePath"]
            wb = xlrd.open_workbook(file_path)
            sheet = wb.sheet_by_index(0)
            number_of_rows, number_of_columns = sheet.nrows, sheet.ncols
            tmx_input, locale = [], None
            for row in range(2, number_of_rows):
                if row == 1:
                    continue
                values = []
                for col in range(number_of_columns):
                    values.append(sheet.cell(row, col).value)
                if row == 0:
                    if values[0] != "Source".strip() or values[1] != "Target".strip() or values[2] != "Locale".strip():
                        return {"message": "Source | Target | Locale - either of these columns is Missing",
                                "status": "FAILED"}
                else:
                    if locale:
                        if str(values[2]).strip() != locale:
                            return {"message": "All the entries must have the same locale", "status": "FAILED"}
                    else:
                        locale = str(values[2]).strip()
                    values_dict = {"src": str(values[0]).strip(), "tgt": str(values[1]).strip(),
                                   "locale": str(values[2]).strip()}
                    tmx_input.append(values_dict)
            tmx_record = {"context": api_input["context"], "sentences": tmx_input}
            if 'userID' in api_input.keys():
                tmx_record["userID"] = api_input["userID"]
            if 'orgID' in api_input.keys():
                tmx_record["orgID"] = api_input["orgID"]
            res = self.push_to_tmx_store(tmx_record)
            if res["status"] == "FAILED":
                return {"message": "bulk creation failed", "status": "FAILED"}
            db_record = tmx_record
            db_record["sentences"], db_record["file"], db_record["timeStamp"] = len(tmx_input), file_path, eval(
                str(time.time()).replace('.', '')[0:13])
            db_record["locale"], db_record["id"] = locale, str(uuid.uuid4())
            repo.tmx_create(db_record)
            db_record_reverse = tmx_record
            reverse_locale_array = str(locale).split("|")
            reverse_locale = str(reverse_locale_array[1]) + "|" + str(reverse_locale_array[0])
            db_record_reverse["sentences"], db_record_reverse["file"], = len(tmx_input), file_path
            db_record_reverse["timeStamp"], db_record_reverse["locale"], db_record["id"] = eval(
                str(time.time()).replace('.', '')[0:13]), reverse_locale, str(uuid.uuid4())
            repo.tmx_create(db_record_reverse)
            log_info("Bulk Create DONE!", None)
            return {"message": "bulk creation successful", "status": "SUCCESS"}
        except Exception as e:
            log_exception("Exception while pushing to TMX: " + str(e), None, e)
            return {"message": "bulk creation failed", "status": "FAILED"}

    # Pushes translations to the tmx.
    def push_to_tmx_store(self, tmx_input):
        log_info("Pushing to TMX......", None)
        try:
            for sentence in tmx_input["sentences"]:
                tmx_records = []
                sentence_types, i = self.fetch_diff_flavors_of_sentence(sentence["src"]), 0
                for sent in sentence_types:
                    tmx_record_pair = {"src": sent, "locale": sentence["locale"], "nmt_tgt": [],
                                       "user_tgt": sentence["tgt"], "context": tmx_input["context"]}
                    if 'userID' in tmx_input.keys():
                        tmx_record_pair["userID"] = tmx_input["userID"]
                    if 'orgID' in tmx_input.keys():
                        tmx_record_pair["orgID"] = tmx_input["orgID"]
                    if i == 0:
                        tmx_record_pair["original"] = True
                    tmx_records.append(tmx_record_pair)
                    i += 1
                reverse_locale_array = str(sentence["locale"]).split("|")
                reverse_locale = str(reverse_locale_array[1]) + "|" + str(reverse_locale_array[0])
                tmx_record_reverse_pair = {"src": sentence["tgt"], "locale": reverse_locale, "nmt_tgt": [],
                                           "user_tgt": sentence["src"], "context": tmx_input["context"]}
                if 'userID' in tmx_input.keys():
                    tmx_record_reverse_pair["userID"] = tmx_input["userID"]
                if 'orgID' in tmx_input.keys():
                    tmx_record_reverse_pair["orgID"] = tmx_input["orgID"]
                tmx_records.append(tmx_record_reverse_pair)
                for tmx_record in tmx_records:
                    hash_dict = self.get_hash_key(tmx_record)
                    for hash_key in hash_dict.keys():
                        tmx_record["hash"] = hash_dict[hash_key]
                        repo.upsert(tmx_record["hash"], tmx_record)
            log_info("Translations pushed to TMX!", None)
            return {"message": "created", "status": "SUCCESS"}
        except Exception as e:
            log_exception("Exception while pushing to TMX: " + str(e), None, e)
            return {"message": "creation failed", "status": "FAILED"}

    def delete_from_tmx_store(self, tmx_input):
        log_info("Deleting to TMX......", None)
        try:
            for sentence in tmx_input["sentences"]:
                tmx_records = []
                sentence_types = self.fetch_diff_flavors_of_sentence(sentence["src"])
                for sent in sentence_types:
                    tmx_record_pair = {"src": sent, "locale": sentence["locale"], "nmt_tgt": [],
                                       "user_tgt": sentence["tgt"], "context": tmx_input["context"]}
                    if 'userID' in tmx_input.keys():
                        tmx_record_pair["userID"] = tmx_input["userID"]
                    if 'orgID' in tmx_input.keys():
                        tmx_record_pair["orgID"] = tmx_input["orgID"]
                    tmx_records.append(tmx_record_pair)
                for tmx_record in tmx_records:
                    hash_dict = self.get_hash_key(tmx_record)
                    for hash_key in hash_dict.keys():
                        repo.delete(hash_dict[hash_key])
            log_info("TMX deleted!", None)
            return {"message": "DELETED", "status": "SUCCESS"}
        except Exception as e:
            log_exception("Exception while deleting TMX: " + str(e), None, e)
            return {"message": "deletion failed", "status": "FAILED"}

    # Method to fetch tmx phrases for a given src
    def get_tmx_phrases(self, user_id, org_id, context, locale, sentence, tmx_level, tmx_file_cache, ctx):
        tmx_record = {"context": context, "locale": locale, "src": sentence}
        if user_id:
            tmx_record["userID"] = user_id
        if org_id:
            tmx_record["orgID"] = org_id
        try:
            tmx_phrases, res_dict = self.tmx_phrase_search(tmx_record, tmx_level, tmx_file_cache, ctx)
            return tmx_phrases, res_dict
        except Exception as e:
            log_exception("Exception while searching tmx from redis: " + str(e), ctx, e)
            return [], {"computed": 0, "redis": 0, "cache": 0}

    # Generates a 3 flavors for a sentence - title case, lowercase and uppercase.
    def fetch_diff_flavors_of_sentence(self, sentence):
        result = []
        org_sentence = str(sentence)
        result.append(org_sentence)
        title = org_sentence.title()
        if org_sentence != title:
            result.append(title)
        small = org_sentence.lower()
        if org_sentence != small:
            result.append(small)
        caps = org_sentence.upper()
        if org_sentence != caps:
            result.append(caps)
        return result

    # Searches for all tmx phrases of a fixed length within a given sentence
    # Uses a custom implementation of the sliding window search algorithm.
    def tmx_phrase_search(self, tmx_record, tmx_level, tmx_file_cache, ctx):
        sentence, tmx_phrases = tmx_record["src"], []
        hopping_pivot, sliding_pivot, i = 0, len(sentence), 1
        computed, r_count, c_count = 0, 0, 0,
        while hopping_pivot < len(sentence):
            phrase = sentence[hopping_pivot:sliding_pivot]
            phrase_size = phrase.split(" ")
            if len(phrase_size) <= tmx_word_length:
                tmx_record["src"] = phrase
                tmx_result, fetch = self.get_tmx_with_fallback(tmx_record, tmx_level, tmx_file_cache, ctx)
                computed += 1
                if tmx_result:
                    tmx_phrases.append(tmx_result[0])
                    phrase_list = phrase.split(" ")
                    hopping_pivot += (1 + len(' '.join(phrase_list)))
                    sliding_pivot = len(sentence)
                    i = 1
                    if fetch is True:
                        r_count += 1
                    else:
                        c_count += 1
                    continue
            sent_list = sentence.split(" ")
            phrase_list = phrase.split(" ")
            reduced_phrase = ' '.join(sent_list[0: len(sent_list) - i])
            sliding_pivot = len(reduced_phrase)
            i += 1
            if hopping_pivot == sliding_pivot or (hopping_pivot - 1) == sliding_pivot:
                hopping_pivot += (1 + len(' '.join(phrase_list)))
                sliding_pivot = len(sentence)
                i = 1
        res_dict = {"computed": computed, "redis": r_count, "cache": c_count}
        return tmx_phrases, res_dict

    # Fetches TMX phrases for a sentence from hierarchical cache
    def get_tmx_with_fallback(self, tmx_record, tmx_level, tmx_file_cache, ctx):
        hash_dict = self.get_hash_key_search(tmx_record, tmx_level)
        if 'USER' in hash_dict.keys():
            if hash_dict["USER"] not in tmx_file_cache.keys():
                tmx_result = repo.search([hash_dict["USER"]])
                if tmx_result:
                    tmx_file_cache[hash_dict["USER"]] = tmx_result
                    return tmx_result, True
            else:
                return tmx_file_cache[hash_dict["USER"]], False
        if 'ORG' in hash_dict.keys():
            if hash_dict["ORG"] not in tmx_file_cache.keys():
                tmx_result = repo.search([hash_dict["ORG"]])
                if tmx_result:
                    tmx_file_cache[hash_dict["ORG"]] = tmx_result
                    return tmx_result, True
            else:
                return tmx_file_cache[hash_dict["ORG"]], False
        if 'GLOBAL' in hash_dict.keys():
            if hash_dict["GLOBAL"] not in tmx_file_cache.keys():
                tmx_result = repo.search([hash_dict["GLOBAL"]])
                if tmx_result:
                    tmx_file_cache[hash_dict["GLOBAL"]] = tmx_result
                    return tmx_result, True
            else:
                return tmx_file_cache[hash_dict["GLOBAL"]], False
        return None, None

    # Replaces TMX phrases in NMT tgt using TMX NMT phrases and LaBSE alignments
    def replace_nmt_tgt_with_user_tgt(self, tmx_phrases, tgt, ctx):
        tmx_without_nmt_phrases, tmx_tgt = [], None
        try:
            for tmx_phrase in tmx_phrases:
                if tmx_phrase["nmt_tgt"]:
                    for nmt_tgt_phrase in tmx_phrase["nmt_tgt"]:
                        if nmt_tgt_phrase in tgt:
                            log_info("(TMX - NMT) Replacing: " + str(nmt_tgt_phrase) + " with: " + str(
                                tmx_phrase["user_tgt"]), ctx)
                            tgt = tgt.replace(nmt_tgt_phrase, tmx_phrase["user_tgt"])
                            break
                else:
                    tmx_without_nmt_phrases.append(tmx_phrase)
            tmx_tgt = tgt
            if tmx_without_nmt_phrases:
                tmx_tgt = self.replace_with_labse_alignments(tmx_without_nmt_phrases, tgt, ctx)
            if tmx_tgt:
                return tmx_tgt
            else:
                return tgt
        except Exception as e:
            log_exception("Exception while replacing nmt_tgt with user_tgt: " + str(e), ctx, e)
            return tgt

    # Replaces phrases in tgt with user tgts using labse alignments and updates nmt_tgt in TMX
    def replace_with_labse_alignments(self, tmx_phrases, tgt, ctx):
        tmx_phrase_dict = {}
        for tmx_phrase in tmx_phrases:
            tmx_phrase_dict[tmx_phrase["src"]] = tmx_phrase
        nmt_req = {"src_phrases": list(tmx_phrase_dict.keys()), "tgt": tgt}
        nmt_req = [nmt_req]
        api_headers = {'Content-Type': 'application/json'}
        nmt_response = requests.post(url=nmt_labse_align_url, json=nmt_req, headers=api_headers)
        if nmt_response:
            if nmt_response.text:
                nmt_response = json.loads(nmt_response.text)
            if 'status' in nmt_response.keys():
                if nmt_response["status"]["statusCode"] != 200:
                    return None
                else:
                    nmt_aligned_phrases = nmt_response["response_body"][0]["aligned_phrases"]
                    if nmt_aligned_phrases:
                        for aligned_phrase in nmt_aligned_phrases.keys():
                            phrase = tmx_phrase_dict[aligned_phrase]
                            log_info("(TMX - LaBSE) Replacing: " + str(
                                nmt_aligned_phrases[aligned_phrase]) + " with: " + str(phrase["user_tgt"]), ctx)
                            tgt = tgt.replace(nmt_aligned_phrases[aligned_phrase], phrase["user_tgt"])
                            modified_nmt_tgt = phrase["nmt_tgt"]
                            modified_nmt_tgt.append(nmt_aligned_phrases[aligned_phrase])
                            phrase["nmt_tgt"] = modified_nmt_tgt
                            repo.upsert(phrase["hash"], phrase)
                    else:
                        log_info("No LaBSE alignments found!", ctx)
                        log_info("LaBSE - " + str(nmt_req), ctx)
                    return tgt
            else:
                return None
        else:
            return None

    # Method to fetch all keys from the redis db
    def get_tmx_data(self, req):
        keys = []
        if "keys" in req.keys():
            keys = req["keys"]
        redis_records = repo.get_all_records(keys)
        if redis_records:
            if "userID" in req.keys():
                filtered = filter(lambda record: self.filter_user_records(record, req["userID"]), redis_records)
                redis_records = list(filtered)
                if "allUserKeys" not in req.keys():
                    filtered = filter(lambda record: self.filter_original_keys(record), redis_records)
                    redis_records = list(filtered)
                elif not req["allUserKeys"]:
                    filtered = filter(lambda record: self.filter_original_keys(record), redis_records)
                    redis_records = list(filtered)
        return redis_records

    def filter_user_records(self, record, user_id):
        if "userID" in record.keys():
            if record["userID"] == user_id:
                return True
            else:
                return False
        else:
            return False

    def filter_original_keys(self, record):
        if "original" in record.keys():
            return record["original"]
        else:
            return False

    # Creates a md5 hash values using userID, orgID, context, locale and src for inserting records.
    def get_hash_key(self, tmx_record):
        hash_dict = {}
        if 'orgID' not in tmx_record.keys() and 'userID' not in tmx_record.keys():
            global_hash = tmx_record["context"] + "__" + tmx_record["locale"] + "__" + tmx_record["src"]
            hash_dict["GLOBAL"] = hashlib.sha256(global_hash.encode('utf-16')).hexdigest()
        if 'orgID' in tmx_record.keys():
            org_hash = tmx_record["orgID"] + "__" + tmx_record["context"] + "__" + tmx_record["locale"] + "__" + \
                       tmx_record["src"]
            hash_dict["ORG"] = hashlib.sha256(org_hash.encode('utf-16')).hexdigest()
        if 'userID' in tmx_record.keys():
            user_hash = tmx_record["userID"] + "__" + tmx_record["context"] + "__" + tmx_record["locale"] + "__" + \
                        tmx_record["src"]
            hash_dict["USER"] = hashlib.sha256(user_hash.encode('utf-16')).hexdigest()
        return hash_dict

    # Creates a md5 hash values using userID, orgID, context, locale and src for searching records.
    def get_hash_key_search(self, tmx_record, tmx_level):
        hash_dict = {}
        if tmx_global_enabled:
            global_hash = tmx_record["context"] + "__" + tmx_record["locale"] + "__" + tmx_record["src"]
            hash_dict["GLOBAL"] = hashlib.sha256(global_hash.encode('utf-16')).hexdigest()
        if tmx_level is None:
            return hash_dict
        if tmx_level == "BOTH":
            if tmx_org_enabled:
                org_hash = tmx_record["orgID"] + "__" + tmx_record["context"] + "__" + tmx_record["locale"] + "__" + \
                           tmx_record["src"]
                hash_dict["ORG"] = hashlib.sha256(org_hash.encode('utf-16')).hexdigest()
            if tmx_user_enabled:
                user_hash = tmx_record["userID"] + "__" + tmx_record["context"] + "__" + tmx_record["locale"] + "__" + \
                            tmx_record["src"]
                hash_dict["USER"] = hashlib.sha256(user_hash.encode('utf-16')).hexdigest()
        elif tmx_level == "USER" and tmx_user_enabled:
            user_hash = tmx_record["userID"] + "__" + tmx_record["context"] + "__" + tmx_record["locale"] + "__" + \
                        tmx_record["src"]
            hash_dict["USER"] = hashlib.sha256(user_hash.encode('utf-16')).hexdigest()
        elif tmx_level == "ORG" and tmx_org_enabled:
            org_hash = tmx_record["orgID"] + "__" + tmx_record["context"] + "__" + tmx_record["locale"] + "__" + \
                       tmx_record["src"]
            hash_dict["ORG"] = hashlib.sha256(org_hash.encode('utf-16')).hexdigest()
        return hash_dict

    # API to create glossary in the system.
    def glossary_create(self, object_in):
        try:
            if 'org' not in object_in.keys():
                return post_error("ORG_NOT_FOUND", "org is mandatory", None)
            if 'context' not in object_in.keys():
                return post_error("CONTEXT_NOT_FOUND", "context is mandatory", None)
            else:
                if 'translations' not in object_in.keys():
                    return post_error("TRANSLATIONS_NOT_FOUND", "Translations are mandatory", None)
                else:
                    if not object_in["translations"]:
                        return post_error("TRANSLATIONS_EMPTY", "Translations cannot be empty", None)
                    else:
                        for translation in object_in["translations"]:
                            if 'src' not in translation.keys():
                                return post_error("SRC_NOT_FOUND", "src is mandatory for every translation", None)
                            if 'tgt' not in translation.keys():
                                return post_error("TGT_NOT_FOUND", "tgt is mandatory for every translation", None)
                            if 'locale' not in translation.keys():
                                return post_error("LOCALE_NOT_FOUND", "locale is mandatory for every translation", None)
            for translation in object_in["translations"]:
                translation["id"] = uuid.uuid4()
                translation["org"] = object_in["org"]
                translation["uploaded_by"] = object_in["userID"]
                translation["created_on"] = eval(str(time.time()).replace('.', '')[0:13])
                repo.glossary_create(translation)
            return {"message": "Glossary created successfully", "status": "SUCCESS"}
        except Exception as e:
            return post_error("GLOSSARY_CREATION_FAILED",
                              "Glossary creation failed due to exception: {}".format(str(e)), None)

    # Method to delete glossary from the db
    def glossary_delete(self, delete_req):
        query = {}
        if 'deleteAll' in delete_req:
            if delete_req["deleteAll"] is True:
                repo.glossary_delete(query)
                return {"message": "Glossary DB cleared successfully", "status": "SUCCESS"}
        if 'ids' in delete_req:
            if delete_req["ids"]:
                query = {"id": {"$in": delete_req["ids"]}}
        if 'userIDs' in delete_req:
            if delete_req["userIDs"]:
                query = {"uploaded_by": {"$in": delete_req["userIDs"]}}
        if 'startDate' in delete_req:
            query["created_on"] = {"$gte": delete_req["startDate"]}
        if 'endDate' in delete_req:
            query["created_on"] = {"$lte": delete_req["endDate"]}
        repo.glossary_delete(query)
        return {"message": "Glossary deleted successfully", "status": "SUCCESS"}

    # Method to search glossary from the glossay db.
    def glossary_get(self, searc_req):
        query, exclude = {}, {'_id': False}
        if 'fetchAll' in searc_req:
            if searc_req["fetchAll"] is True:
                return repo.glossary_search(query, exclude)
        if 'ids' in searc_req:
            if searc_req["ids"]:
                query = {"id": {"$in": searc_req["ids"]}}
        if 'src' in searc_req:
            if searc_req["src"]:
                query["src"] = {"$in": searc_req["src"]}
        if 'tgt' in searc_req:
            if searc_req["tgt"]:
                query["tgt"] = {"$in": searc_req["tgt"]}
        if 'locale' in searc_req:
            if searc_req["locale"]:
                query["locale"] = {"$in": searc_req["locale"]}
        if 'org' in searc_req:
            if searc_req["org"]:
                query["org"] = {"$in": searc_req["org"]}
        if 'userID' in searc_req:
            if searc_req["userIDs"]:
                query["uploaded_by"] = {"$in": searc_req["userIDs"]}
        if 'startDate' in searc_req:
            query["created_on"] = {"$gte": searc_req["startDate"]}
        if 'endDate' in searc_req:
            query["created_on"] = {"$lte": searc_req["endDate"]}
        return repo.glossary_search(query, exclude)
