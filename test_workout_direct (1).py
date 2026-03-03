"""
Diagnostic script to test workout logging directly
Run this with: python test_workout_direct.py
"""

import sys
sys.path.insert(0, '.')

from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.workout import WorkoutLogCreate
from datetime import datetime, timezone

# Test imports
print("=" * 50)
print("TESTING IMPORTS")
print("=" * 50)

try:
    from app.services import workout_service
    print("✅ workout_service imported")
except Exception as e:
    print(f"❌ Failed to import workout_service: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from app.services import pet_service
    print("✅ pet_service imported")
except Exception as e:
    print(f"❌ Failed to import pet_service: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from app.services import food_service
    print("✅ food_service imported")
except Exception as e:
    print(f"❌ Failed to import food_service: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from app.models.user import User
    print("✅ User model imported")
except Exception as e:
    print(f"❌ Failed to import User: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("TESTING WORKOUT LOGGING")
print("=" * 50)

# Get a database session
db = next(get_db())

# Get first user
user = db.query(User).first()
if not user:
    print("❌ No users in database!")
    sys.exit(1)

print(f"✅ Found user: {user.username} (ID: {user.id})")
print(f"   Current coins: {user.coins}")

# Create test workout
workout_data = WorkoutLogCreate(
    exercise_name="Test Workout",
    muscle_group="chest",
    duration_mins=30,
    sets=3,
    reps=10,
    calories_burned=200
)

print(f"\n🏋️ Logging workout: {workout_data.exercise_name}")

# Try to log workout
try:
    log, xp_awarded = workout_service.log_workout(db, user.id, workout_data)
    print(f"✅ Workout logged successfully!")
    print(f"   Workout ID: {log.id}")
    print(f"   XP Awarded: {xp_awarded}")
except Exception as e:
    print(f"❌ Failed to log workout: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check if coins were awarded
db.refresh(user)
print(f"\n💰 User coins after workout: {user.coins}")

# Check pet XP
try:
    pet = pet_service.get_pet_by_user_id(db, user.id)
    print(f"🐱 Pet XP: {pet.xp}, Level: {pet.level}")
except Exception as e:
    print(f"⚠️  Could not get pet: {e}")

print("\n" + "=" * 50)
print("TESTING STREAK CALCULATION")
print("=" * 50)

try:
    streak = workout_service.get_streak(db, user.id)
    print(f"✅ Streak calculated successfully!")
    print(f"   Current streak: {streak['current_streak']}")
    print(f"   Longest streak: {streak['longest_streak']}")
except Exception as e:
    print(f"❌ Failed to calculate streak: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)

db.close()
