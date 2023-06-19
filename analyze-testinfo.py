import json

# {"inviter_id": "", "item_id": "", "voter_id": "", "timestamp": "2021-12-27 00:00:15"}
with open('raw/item_share_train_info.json', 'r') as f:
    item_share = json.load(f)
print(f"{len(item_share)} item_share")

# {"user_id": "", "user_gender": 0, "user_age": 3, "user_level": 6}
with open('raw/user_info.json', 'r') as f:
    user_info = json.load(f)
print(f"{len(user_info)} user_info")

# {"item_id": "", "cate_id": "", "cate_level1_id": "16", "brand_id": "", "shop_id": ""}
with open('raw/item_info.json', 'r') as f:
    item_info = json.load(f)
print(f"{len(item_info)} item_info")

# 'userid2num.json', 'usernum2id.json', 'itemid2num.json', 'itemnum2id.json'

with open('processed/userid2num.json', 'r') as f:
    userid2num = json.load(f)

with open('processed/usernum2id.json', 'r') as f:
    usernum2id = json.load(f)

with open('processed/itemid2num.json', 'r') as f:
    itemid2num = json.load(f)

with open('processed/itemnum2id.json', 'r') as f:
    itemnum2id = json.load(f)

for i in item_share:
    i["inviter_id"] = userid2num[i["inviter_id"]]
    i["item_id"] = itemid2num[i["item_id"]]
    i["voter_id"] = userid2num[i["voter_id"]]


inviter_voter_dict_count = {}
for i in item_share:
    inviter_id = i["inviter_id"]
    voter_id = i["voter_id"]
    if inviter_id in inviter_voter_dict_count:
        if voter_id in inviter_voter_dict_count[inviter_id]:
            inviter_voter_dict_count[inviter_id][voter_id] += 1
        else:
            inviter_voter_dict_count[inviter_id][voter_id] = 1
    else:
        tt = {}
        tt[voter_id] = 1
        inviter_voter_dict_count[inviter_id] = tt

voter_item_dict = {}
for i in item_share:
    voter_id = i["voter_id"]
    item_id = i["item_id"]
    if voter_id in voter_item_dict:
        voter_item_dict[voter_id].add(item_id)
    else:
        t = set()
        t.add(item_id)
        voter_item_dict[voter_id] = t


sorted_vid = sorted(voter_item_dict.items(),key=lambda s:len(s[1]), reverse=True)
top_voter = [sorted_vid[0][0], sorted_vid[2][0], sorted_vid[3][0], sorted_vid[4][0], sorted_vid[5][0]]
print([len(ii[1]) for ii in sorted_vid[:5]])
print(top_voter)

# {"inviter_id": "", "item_id": "", "voter_id": "", "timestamp": "2021-12-27 00:00:15"}
with open('raw/item_share_preliminary_test_info.json', 'r') as f:
    item_share_test = json.load(f)
print(f"{len(item_share_test)} item_share_test")


A_inviters_index = []
for line in item_share_test:
    A_inviters_index.append(int(userid2num[line['inviter_id']]))


with open('./processed/usernum2id.json', 'r') as load_f:
    usernum2id = json.load(load_f)
submission_A = []
for i in range(len(A_inviters_index)):
    idx = A_inviters_index[i]
    topKlist = None
    if idx in inviter_voter_dict_count:
        ll = len(inviter_voter_dict_count[idx])
        dd = sorted(inviter_voter_dict_count[idx].items(),key=lambda s:s[1], reverse=True)
        da = [kk[0] for kk in dd]
        if len(da) >= 5:
            topKlist = da[:5]
        else:
            ij = 0
            while len(da) < 5:
                if top_voter[ij] not in da:
                    da.append(top_voter[ij])
                ij+=1
            topKlist = da
    else:
        topKlist = top_voter
    assert(len(set(topKlist)) == 5)
    candidate_voter_list = [usernum2id[str(top_voter_index)] for top_voter_index in topKlist]
    submission_A.append({'triple_id': str('%06d' % i), 'candidate_voter_list': candidate_voter_list})
with open('submission_A_wtf.json', 'w') as f:
    json.dump(submission_A, f)
