from views.ticket import generate_search_dict
# 根据传递的条件，生成最终的搜索条件
search = {
    "search_type": "condition",
    "operate": "and",
    "page": 1,
    "page_size": 20,
    "search": '',
    "category": "all",
    "data": [{
        "key": "workflow_ids",
        "key_name": "工作流ids",
        "action": "exact",
        "action_name": "等于",
        "value": 1,
        "value_name": "VPN申请",
        "field_type_id": 45,
        "field_type": "basic",
        "sort": 10
    }, {
        "key": "gmt_created",
        "key_name": "创建时间",
        "action": "between",
        "action_name": "区间",
        "value": ["2024-04-01 00:00:00", "2024-04-30 00:00:00"],
        "value_name": "2024-04-01 00:00 ~ 2024-04-30 00:00",
        "field_type_id": 30,
        "field_type": "basic",
        "sort": 20
    }, {
        "key": "title",
        "key_name": "标题",
        "action": "exact",
        "action_name": "等于",
        "value": "all",
        "value_name": "all",
        "field_type": "basic",
        "field_type_id": 5,
        "sort": 30
    }]
}


print(generate_search_dict(search))
