import random

def generate_training_plan(user_profile, history=None):
    goal = user_profile.get("goal", "поддержание")
    level = user_profile.get("fitness_level", "начинающий")
    time = user_profile.get("available_time_min", 30)

    exercises_db = {
        "похудение": [
            {"name": "прыжки на месте", "type": "кардио", "duration_min": 3},
            {"name": "берпи", "type": "кардио", "duration_min": 4},
            {"name": "планка", "type": "силовое", "duration_min": 2},
            {"name": "приседания", "type": "силовое", "duration_min": 3},
            {"name": "выпады", "type": "силовое", "duration_min": 3},
            {"name": "скручивания на пресс", "type": "силовое", "duration_min": 2},
            {"name": "прыжки через скакалку", "type": "кардио", "duration_min": 5},
            {"name": "альпинист", "type": "кардио", "duration_min": 3},
            {"name": "прыжки звёздочка", "type": "кардио", "duration_min": 3},
            {"name": "отжимания", "type": "силовое", "duration_min": 3}
        ],
        "набор массы": [
            {"name": "жим лёжа", "type": "силовое", "duration_min": 4},
            {"name": "приседания с весом", "type": "силовое", "duration_min": 5},
            {"name": "становая тяга", "type": "силовое", "duration_min": 5},
            {"name": "подтягивания", "type": "силовое", "duration_min": 4},
            {"name": "жим гантелей", "type": "силовое", "duration_min": 4},
            {"name": "сгибания рук на бицепс", "type": "силовое", "duration_min": 3},
            {"name": "разгибания рук на трицепс", "type": "силовое", "duration_min": 3},
            {"name": "тяга верхнего блока", "type": "силовое", "duration_min": 4},
            {"name": "подъемы на носки", "type": "силовое", "duration_min": 3},
            {"name": "жим ногами", "type": "силовое", "duration_min": 4}
        ],
        "поддержание": [
            {"name": "легкий бег", "type": "кардио", "duration_min": 10},
            {"name": "отжимания", "type": "силовое", "duration_min": 3},
            {"name": "пресс", "type": "силовое", "duration_min": 3},
            {"name": "планка", "type": "силовое", "duration_min": 2},
            {"name": "приседания без веса", "type": "силовое", "duration_min": 3},
            {"name": "прыжки на месте", "type": "кардио", "duration_min": 3},
            {"name": "велосипед (упражнение)", "type": "силовое", "duration_min": 3},
            {"name": "прыжки звёздочка", "type": "кардио", "duration_min": 3},
            {"name": "разведение рук с гантелями", "type": "силовое", "duration_min": 3},
            {"name": "растяжка", "type": "силовое", "duration_min": 5}
        ]
    }

    proportions = {
        "похудение": {"кардио": 0.7, "силовое": 0.3},
        "набор массы": {"кардио": 0.2, "силовое": 0.8},
        "поддержание": {"кардио": 0.5, "силовое": 0.5}
    }

    cardio_ratio = proportions.get(goal, {"кардио":0.5, "силовое":0.5})["кардио"]
    strength_ratio = proportions.get(goal, {"кардио":0.5, "силовое":0.5})["силовое"]

    if level == "начинающий":
        sets, reps, rest = 2, 10, 60
    elif level == "средний":
        sets, reps, rest = 3, 12, 45
    else:
        sets, reps, rest = 4, 15, 30

    exercises = exercises_db.get(goal, exercises_db["поддержание"])
    random.shuffle(exercises)

    cardio_exercises = [ex for ex in exercises if ex["type"] == "кардио"]
    strength_exercises = [ex for ex in exercises if ex["type"] == "силовое"]

    plan = []
    total_time = 0

    if time <= 20:
        total_time = 2
    elif time <= 40:
        total_time = 4
    elif time <= 60:
        total_time = 5
    else:
        total_time = 10

    plan.append({"name": "Разминка",
                 "text": f"1. Разминка - {total_time} минут"
                 })

    cardio_time_target = time * cardio_ratio
    strength_time_target = time * strength_ratio

    def add_exercises(ex_list, time_target):
        nonlocal total_time, plan
        for coun, ex in  enumerate(ex_list, 1):
            ex_time = ex["duration_min"] * sets + (sets -1) * (rest / 60)
            if total_time + ex_time > time:
                break
            if ex_time <= time_target:
                plan.append({"name": ex["name"],
                             "sets": sets,
                             "reps": reps,
                             "rest_sec": rest,
                             "text": f"{coun}. {ex['name'].capitalize()} — {sets} подхода по {reps} повторений (отдых: {rest} сек)"
                })
                total_time += ex_time
                time_target -= ex_time

    add_exercises(cardio_exercises, cardio_time_target)
    add_exercises(strength_exercises, strength_time_target)

    adapted_plan = []
    for coun, exercise in enumerate(plan, 1):
        if exercise["name"] != "Разминка":
            times_done = history.count(exercise["name"]) if history else 0
            exercise_copy = exercise.copy()

            exercise_copy["reps"] = exercise["reps"] + times_done * 2
            exercise_copy["text"] = f"{coun}. {exercise["name"].capitalize()} — {exercise["sets"]} подхода по {exercise_copy["reps"]} повторений (отдых: {rest} сек)"

            adapted_plan.append(exercise_copy)
        else:
            adapted_plan.append(exercise)

    return adapted_plan

