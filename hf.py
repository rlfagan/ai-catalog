#!/usr/bin/env python3
import os
import json
import time
from huggingface_hub import HfApi


RATE_LIMIT_SLEEP = 0.2  # adjust if rate-limited


def obj_to_dict(obj):
    """Convert HF metadata objects to a clean dict."""
    out = {}
    for k in dir(obj):
        if k.startswith("_"):
            continue
        try:
            v = getattr(obj, k)
        except Exception:
            continue
        if callable(v):
            continue
        out[k] = v
    return out


def dump_iter(name, iterator, output_file):
    count = 0
    with open(output_file, "w", encoding="utf-8") as f:
        for item in iterator:
            record = obj_to_dict(item)
            f.write(json.dumps(record, default=str) + "\n")
            count += 1
            if count % 100 == 0:
                print(f"[{name}] wrote {count} entries...")
            time.sleep(RATE_LIMIT_SLEEP)
    print(f"[{name}] DONE -> {output_file} ({count} total)")


def main():
    token = os.getenv("HUGGINGFACE_HUB_TOKEN")
    api = HfApi(token=token)

    print("Using token?" , bool(token))

    print("\n=== MODELS ===")
    dump_iter(
        "models",
        api.list_models(full=True),
        "hf_models.jsonl",
    )

    print("\n=== DATASETS ===")
    dump_iter(
        "datasets",
        api.list_datasets(full=True),
        "hf_datasets.jsonl",
    )

    print("\n=== SPACES ===")
    dump_iter(
        "spaces",
        api.list_spaces(full=True),
        "hf_spaces.jsonl",
    )

    print("\nAll done!")


if __name__ == "__main__":
    main()
