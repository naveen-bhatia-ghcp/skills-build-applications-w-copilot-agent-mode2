from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        # Delete all objects individually to avoid unhashable model errors
        for model in [Activity, Workout, Leaderboard, User, Team]:
            for obj in model.objects.all():
                if obj.pk:
                    obj.delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create users

        users = []
        user_data = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc, 'is_superhero': True},
        ]
        for u in user_data:
            user = User(**u)
            user.save()
            users.append(user)

        # Create activities
        Activity.objects.create(user=users[0], activity_type='Running', duration_minutes=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Cycling', duration_minutes=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type='Swimming', duration_minutes=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Yoga', duration_minutes=40, date=timezone.now().date())

        # Create workouts
        workout1 = Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes')
        workout2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility')
        workout1.suggested_for.set([marvel, dc])
        workout2.suggested_for.set([dc])

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, total_points=100)
        Leaderboard.objects.create(team=dc, total_points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
