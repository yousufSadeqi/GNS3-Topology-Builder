import requests   

SERVER = "http://127.0.0.1:3080"
AUTH = ("admin", "K6fbnTZ9GqYmu6fvkDx3pY6NgtHYtPLadr79u2HT6WLjt2RUlyZJg0T7hy3qa8an")
PROJECT_NAME = "Ai generated Topology"


def get_json(url):
    return requests.get(url, auth=AUTH).json()


def post_json(url, payload):
    return requests.post(url, json=payload, auth=AUTH).json()

# Templates
templates = get_json(f"{SERVER}/v2/templates")
print(templates) 
find = lambda name: next(t for t in templates if name.lower() in t["name"].lower())

router_tpl = find("c7200")
switch_tpl = find("ethernet switch")
pc_tpl = find("vpcs")

image_name = router_tpl.get("image", "c7200-advipservicesk9-mz.152-4.S5.image")


# Project
projects = get_json(f"{SERVER}/v2/projects")
existing = next((p for p in projects if p["name"].strip().lower() == PROJECT_NAME.lower()), None)
PROJECT_ID = existing["project_id"] if existing else post_json(f"{SERVER}/v2/projects", {"name": PROJECT_NAME})["project_id"]

post_json(f"{SERVER}/v2/projects/{PROJECT_ID}/open", {})


# Node creation
def create_router(name, x, y):
    return post_json(f"{SERVER}/v2/projects/{PROJECT_ID}/nodes", {
        "name": name,
        "template_id": router_tpl["template_id"],
        "node_type": "dynamips",
        "compute_id": "local",
        "symbol": router_tpl.get("symbol"),
        "properties": {
            "platform": "c7200",
            "image": image_name,
            "ram": 512,
            "slot1": "C7200-IO-FE",
            "slot2": "C7200-IO-FE"
        },
        "x": x, "y": y
    })


def create_switch(name, x, y):
    return post_json(f"{SERVER}/v2/projects/{PROJECT_ID}/nodes", {
        "name": name,
        "template_id": switch_tpl["template_id"],
        "node_type": switch_tpl["template_type"],
        "compute_id": "local",
        "symbol": switch_tpl.get("symbol"),
        "x": x, "y": y
    })


def create_pc(name, x, y):
    return post_json(f"{SERVER}/v2/projects/{PROJECT_ID}/nodes", {
        "name": name,
        "template_id": pc_tpl["template_id"],
        "node_type": pc_tpl["template_type"],
        "compute_id": "local",
        "symbol": pc_tpl.get("symbol"),
        "x": x, "y": y
    })


# Build topology
r1 = create_router("R1", -300, 0)
r2 = create_router("R2", 0, 0)
r3 = create_router("R3", 300, 0)
# Additional routers, switches, and PCs (same style as above)
r4 = create_router("R4", 600, 0)
r5 = create_router("R5", 900, 0)

sw1 = create_switch("SW1", -300, 200)
sw2 = create_switch("SW2", 0, 200)
sw3 = create_switch("SW3", 300, 200)
sw4 = create_switch("SW4", 600, 200)
sw5 = create_switch("SW5", 900, 200)

pc1 = create_pc("PC1", -400, 400)
pc2 = create_pc("PC2", -200, 400)
pc3 = create_pc("PC3", -100, 400)
pc4 = create_pc("PC4", 100, 400)
pc5 = create_pc("PC5", 200, 400)
pc6 = create_pc("PC6", 400, 400)
pc7  = create_pc("PC7", 500, 400)
pc8  = create_pc("PC8", 700, 400)
pc9  = create_pc("PC9", 800, 400)
pc10 = create_pc("PC10", 1000, 400)

# Links
def link(a, ap, b, bp, a_adapter=0, b_adapter=0):
    post_json(f"{SERVER}/v2/projects/{PROJECT_ID}/links", {
        "nodes": [
            {"node_id": a, "adapter_number": a_adapter, "port_number": ap},
            {"node_id": b, "adapter_number": b_adapter, "port_number": bp}
        ]
    })


link(r1["node_id"], 0, sw1["node_id"], 0)
link(r2["node_id"], 0, sw2["node_id"], 0)
link(r3["node_id"], 0, sw3["node_id"], 0)
# Router <-> Switch links
link(r4["node_id"], 0, sw4["node_id"], 0)
link(r5["node_id"], 0, sw5["node_id"], 0)

link(r1["node_id"], 0, r2["node_id"], 0, a_adapter=1, b_adapter=1)
link(r2["node_id"], 0, r3["node_id"], 0, a_adapter=2, b_adapter=1)
link(r3["node_id"], 0, r4["node_id"], 0, a_adapter=2, b_adapter=1)
link(r4["node_id"], 0, r5["node_id"], 0, a_adapter=2, b_adapter=1)

link(sw1["node_id"], 1, pc1["node_id"], 0)
link(sw1["node_id"], 2, pc2["node_id"], 0)
link(sw2["node_id"], 1, pc3["node_id"], 0)
link(sw2["node_id"], 2, pc4["node_id"], 0)
link(sw3["node_id"], 1, pc5["node_id"], 0)
link(sw3["node_id"], 2, pc6["node_id"], 0)
link(sw4["node_id"], 1, pc7["node_id"], 0)
link(sw4["node_id"], 2, pc8["node_id"], 0)
link(sw5["node_id"], 1, pc9["node_id"], 0)
link(sw5["node_id"], 2, pc10["node_id"], 0)

print("Topology built.")