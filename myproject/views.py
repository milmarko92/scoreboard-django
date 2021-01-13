import json
from array import array
from typing import Dict

from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
import datetime

from myproject.models import Entry, Vote, Edition


def cast_vote(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        name = json_data.get('name')
        if not name:
            return HttpResponse("You didn't choose a name", status=400)
        vote_list = json_data.get('votes')
        edition_id = json_data.get('edition')
        edition = Edition.objects.get(id=edition_id)
        print(request.body)
        print(name, vote_list)
        for vote in vote_list:
            code = vote.get("code")
            rank = vote.get("rank")
            entry = Entry.objects.get(code=code)
            if edition:
                _, created = Vote.objects.update_or_create(voter=name, entry=entry, edition=edition, defaults={"score": rank})
            else:
                _, created = Vote.objects.update_or_create(voter=name, entry=entry, defaults={"score": rank})

        print(f"vote recorded from {name}")

    html = f"Thank you for your vote"
    return HttpResponse(html)


def break_tie(a, b):
    """
    return true if a one WINS the tiebreak
    """
    a_top10s = sum(a["count_of_each_rank"])
    b_top10s = sum(b["count_of_each_rank"])
    if a_top10s != b_top10s:
        return a_top10s > b_top10s

    for i in range(10):
        if a["count_of_each_rank"][i] != b["count_of_each_rank"][i]:
            return a["count_of_each_rank"][i] > b["count_of_each_rank"][i]

    return a


def rank_with_tie_break(result):
    result.sort(key=lambda x: x["score"])
    for i in range(len(result)-1):
        if result[i]["score"] == result[i+1]["score"]:
            if not break_tie(result[i], result[i+1]):
                x = result[i]
                result[i] = result[i+1]
                result[i+1] = x
        result[i]["rank"] = i + 1
        del result[i]["count_of_each_rank"]


def _get_entry_scores(entry: Entry, edition_id: int):
    votes = entry.vote_set.filter(edition__id=edition_id)
    twelve_point_sum = 0
    sum = 0
    count = 0
    count_of_each_rank = [0,0,0,0,0,0,0,0,0,0]
    names = set()
    for rank in votes:
        sum += rank.score
        score = 0
        names.add(rank.voter)
        try:
            score = twelve_point_map[rank.score-1]
            count_of_each_rank[rank.score-1] += 1
        except Exception:
            pass
        twelve_point_sum += score
        count += 1

    return {"score": float(sum)/count if count > 0 else 0, "twelvePointScore": twelve_point_sum, "count_of_each_rank": count_of_each_rank}, names


def get_result(request, edition):
    if request.method == "GET":
        results = []
        all_voters = set()
        for entry in Entry.objects.filter(vote__edition_id=edition).distinct():
            print([entry.vote_set.all()])
            code = entry.code
            avg_score, voters = _get_entry_scores(entry, edition)
            avg_score["entry"] = code
            results.append(avg_score)
            all_voters = all_voters.union(voters)
        print(results)

        rank_with_tie_break(results)

        return JsonResponse({"results": results, "voters": ",".join(all_voters)})
    return HttpResponse("wrong")


twelve_point_map = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]


def download_link(request, edition):
    all_votes = Vote.objects.filter(edition__id=edition)
    votes_dict = {}
    voters = set()
    entries = set()
    for vote in all_votes:
        entry = vote.entry.code
        voter = vote.voter
        voters.add(voter)
        entries.add(entry)
        if not votes_dict.get(entry):
            votes_dict[entry] = {}
        votes_dict[entry][voter] = vote.score
    output = "country," + ",".join(voters) + "\n"
    for c in entries:
        output += f"{c},"
        sum = 0
        cnt = 0
        for v in voters:
            print(f"{c}, {v}, {votes_dict[c][v]}")
            output += str(votes_dict[c][v]) + ","
            sum += votes_dict[c][v]
            cnt += 1
        avg = sum/cnt if cnt > 0 else 0
        output += f"{avg}\n"
    print(output)
    return HttpResponse(output, content_type='text/csv')