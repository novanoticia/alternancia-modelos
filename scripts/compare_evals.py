#!/usr/bin/env python3
"""Compare one native/plugin pair of reported observations; never call a model."""

import argparse
import json
import math
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, expected, path):
    require(isinstance(value, dict), f"{path}: expected an object")
    require(set(value) == set(expected.split()), f"{path}: expected fields {expected}")


def number(value, path, nullable=False, integer=False):
    if value is None and nullable:
        return
    try:
        valid = type(value) in (int, float) and math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    require(valid,
            f"{path}: expected a finite nonnegative number")
    require(not integer or type(value) is int, f"{path}: expected an integer")


def text(value, path):
    require(isinstance(value, str) and bool(value.strip()), f"{path}: expected nonempty text")


def strings(value, path, nonempty=False):
    require(isinstance(value, list) and (not nonempty or bool(value)), f"{path}: expected a list")
    for item in value:
        text(item, path)
    require(len(value) == len(set(value)), f"{path}: duplicate entries")


def validate(data):
    fields(data, "schema_version synthetic experiment_id task_id pair_id policy runs", "record")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unsupported schema_version")
    require(type(data["synthetic"]) is bool, "synthetic must be explicitly true or false")
    for key in ("experiment_id", "task_id", "pair_id"):
        text(data[key], key)
    policy = data["policy"]
    fields(policy, "min_quality_gain equivalence_margin max_time_increase_pct "
           "max_resource_increase_pct resource_metric currency time_limit_seconds resource_limit", "policy")
    for key in ("min_quality_gain", "equivalence_margin", "max_time_increase_pct", "max_resource_increase_pct"):
        number(policy[key], key)
    require(0 <= policy["equivalence_margin"] < policy["min_quality_gain"] <= 100,
            "Require 0 <= equivalence_margin < min_quality_gain <= 100")
    require(policy["resource_metric"] in ("tokens", "cost"), "resource_metric must be tokens or cost")
    currency = policy["currency"]
    require(currency is None or (isinstance(currency, str) and len(currency) == 3
            and currency.isascii() and currency.isalpha() and currency.isupper()),
            "policy.currency must be a three-letter code or null")
    require(policy["resource_metric"] != "cost" or currency is not None,
            "A cost comparison requires policy.currency")
    number(policy["time_limit_seconds"], "time_limit_seconds", nullable=True)
    number(policy["resource_limit"], "resource_limit", nullable=True,
           integer=policy["resource_metric"] == "tokens")
    fields(data["runs"], "native plugin", "runs")
    for condition, run in data["runs"].items():
        fields(run, "setup completed requirements_met quality wall_seconds tokens cost currency "
               "calls models_observed evidence", condition)
        fields(run["setup"], "host primary_model effort context_id available_models tools rubric_id "
               "budget_id native_delegation_allowed", f"{condition}.setup")
        for key in ("host", "primary_model", "effort", "context_id", "rubric_id", "budget_id"):
            text(run["setup"][key], f"{condition}.setup.{key}")
        strings(run["setup"]["available_models"], "available_models", nonempty=True)
        strings(run["setup"]["tools"], "tools")
        require(run["setup"]["native_delegation_allowed"] is True,
                "Keep native delegation available in both conditions")
        for key in ("completed", "requirements_met"):
            require(type(run[key]) is bool, f"{condition}.{key}: expected boolean")
        for key in ("quality", "wall_seconds", "cost", "tokens", "calls"):
            number(run[key], f"{condition}.{key}", nullable=True, integer=key in ("tokens", "calls"))
        require(run["quality"] is None or run["quality"] <= 100, "quality must be between 0 and 100")
        require(run["currency"] is None or (isinstance(run["currency"], str)
                and len(run["currency"]) == 3 and run["currency"].isascii()
                and run["currency"].isalpha() and run["currency"].isupper()), "Use a three-letter currency code or null")
        require(run["cost"] is None or run["currency"] is not None, "A measured cost requires currency")
        strings(run["models_observed"], "models_observed")
        strings(run["evidence"], "evidence", nonempty=True)


def compare(data):
    validate(data)
    native, plugin = data["runs"]["native"], data["runs"]["plugin"]
    policy = data["policy"]
    metric = policy["resource_metric"]
    result = {
        "schema_version": 1,
        "experiment_id": data["experiment_id"], "task_id": data["task_id"], "pair_id": data["pair_id"],
        "source": "synthetic" if data["synthetic"] else "reported_observations",
        "scope": "single_pair", "resource_metric": metric,
        "note": "Clasificación de un par según datos aportados; no verifica las fuentes ni demuestra una mejora general.",
    }

    def finish(status, reason):
        return {**result, "status": status, "reason": reason}

    left, right = dict(native["setup"]), dict(plugin["setup"])
    for key in ("available_models", "tools"):
        left[key], right[key] = sorted(left[key]), sorted(right[key])
    if left != right:
        return finish("inconclusive", "Las condiciones declaradas de ejecución no son equivalentes.")
    if not native["completed"] or not plugin["completed"]:
        return finish("inconclusive", "Falta una ejecución completa del par.")
    if not plugin["requirements_met"]:
        return finish("regression", "El plugin incumple al menos un requisito obligatorio.")
    if metric == "cost" and any(run["cost"] is not None and run["currency"] != policy["currency"]
                                for run in (native, plugin)):
        return finish("inconclusive", "La moneda de las observaciones no coincide con la del presupuesto.")
    for field, limit_key in (("wall_seconds", "time_limit_seconds"), (metric, "resource_limit")):
        limit = policy[limit_key]
        if limit is not None and plugin[field] is not None and plugin[field] > limit:
            return finish("regression", f"El plugin supera el límite absoluto de {field}.")
    if any(run[key] is None for run in (native, plugin) for key in ("quality", "wall_seconds", metric)):
        return finish("inconclusive", "Faltan calidad, tiempo o consumo de la métrica elegida; null no significa cero.")
    gain = plugin["quality"] - native["quality"]
    result["differences"] = {
        "quality_points": gain,
        "wall_seconds": plugin["wall_seconds"] - native["wall_seconds"],
        metric: plugin[metric] - native[metric],
    }
    if native["requirements_met"] and gain < -policy["equivalence_margin"]:
        return finish("regression", "La pérdida de calidad excede el margen declarado de equivalencia.")
    acceptable = (plugin["wall_seconds"] <= native["wall_seconds"] * (1 + policy["max_time_increase_pct"] / 100)
                  and plugin[metric] <= native[metric] * (1 + policy["max_resource_increase_pct"] / 100))
    if acceptable and (gain >= policy["min_quality_gain"] or not native["requirements_met"]):
        return finish("observed_benefit", "Mejor calidad o cumplimiento, con recursos adicionales dentro de los límites declarados.")
    equivalent = native["requirements_met"] and abs(gain) <= policy["equivalence_margin"]
    no_more_resources = plugin["wall_seconds"] <= native["wall_seconds"] and plugin[metric] <= native[metric]
    less_resources = plugin["wall_seconds"] < native["wall_seconds"] or plugin[metric] < native[metric]
    if equivalent and no_more_resources and less_resources:
        return finish("observed_benefit", "Calidad equivalente con reducción de tiempo o consumo y sin aumento del otro.")
    return finish("no_clear_benefit", "Este par no cumple ninguna de las dos condiciones de mejora predefinidas.")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="JSON record with one comparable native/plugin pair")
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        output = compare(data)
    except (OSError, ValueError, TypeError, OverflowError, RecursionError) as error:
        print(f"Invalid evaluation record: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
