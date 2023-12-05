from django.test import TestCase                                # For test suite to work.
from django.urls import reverse
from .models import *                                           # Get models.
from .forms import *
from django.core.management import call_command
from django.utils import timezone
import random
from django.contrib.auth.models import User
from django.test.client import Client

class HelperFunctionTestClass(TestCase):
    # Helper Methods
    def get_location(self):
        identifier = random.randrange(100)
        location_data = {'title': f'Test Location {identifier}', 'clue': f'Clue {identifier}', 'lat': round(random.uniform(0,100), 14), 'long': round(random.uniform(0,100), 14), 'description': f'Test Description {identifier}', 'answer': f'Test Answer {identifier}'}
        return location_data

    def get_quest(self):
        identifier = random.randrange(100)
        quest_data = {'title': f'Test Quest {identifier}', 'cache_type': 'Traditional'}
        return quest_data

    def create_author(self):
        return Author.objects.create()

    def create_quest(self, title='Test Quest', pub_date=timezone.now(), cache_type='Traditional'):
        author = self.create_author()
        return Quest.objects.create(title=title, pub_date=pub_date, author=author, cache_type=cache_type)

    def create_location(self, title='Test Location', clue='Example Clue', lat='11.11',long='22.22'):
        quest = self.create_quest()
        return Location.objects.create(quest=quest, title=title, clue=clue, lat=lat, long=long)


class QuestFormTests(HelperFunctionTestClass):
    # Test Methods
    def test_quest_form_valid(self):
        quest_data = self.get_quest()
        quest_form = QuestForm(data=quest_data)
        self.assertTrue(quest_form.is_valid())

    def test_location_form_valid(self):
        location_data = self.get_location()
        location_form = LocationForm(location_data)
        self.assertTrue(location_form.is_valid())
    
    def test_location_string(self):
        location = self.create_location()
        self.assertTrue(isinstance(location, Location))
        self.assertEqual(location.__str__(),location.title)

    def test_quest_string(self):
        quest = self.create_quest()
        self.assertTrue(isinstance(quest, Quest))
        self.assertEqual(quest.__str__(),quest.title)


class SiteNavigationTests(HelperFunctionTestClass):
    # Setup admin and user once.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.staff_user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        cls.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=False)
        
    def test_user_access(self):
        self.client.login(username='testuser', password='testpassword')
        self.assertEqual(self.client.get(reverse('maps:index')).status_code, 200)
        self.assertEqual(self.client.get(reverse('maps:create')).status_code, 200)
        self.assertEqual(self.client.get(reverse('maps:approve')).status_code, 302)
        self.assertEqual(self.client.get(reverse('maps:search')).status_code, 200)
        self.assertEqual(self.client.get(reverse('maps:leaderboard')).status_code, 200)
        self.assertEqual(self.client.get(reverse('maps:myQuests')).status_code, 200)

    def test_staff_access(self):
        self.client.login(username='staffuser', password='staffpassword')
        self.assertEqual(self.client.get(reverse('maps:approve')).status_code, 200)


class FormTests(HelperFunctionTestClass):
    def setUp(self):
        self.client = Client()

    # def test_create_form_valid_submission(self):
    #     # Test form
    #     form_data = {
    #         'title': 'test_quest_title',
    #         'location-title': 'test_location_title',
    #         'clue': 'TestClue',
    #         'lat': 10.10101,
    #         'long': -11.10101,
    #         'description': 'test_description',
    #         'answer': 'test_answer'
    #     }

    #     quest = self.create_quest(title='test_quest_title')

    #     url = reverse('maps:create')
    #     self.assertEqual(self.client.get(reverse('maps:create')).status_code, 200)

    #     response = self.client.post(url, form_data)
    #     self.assertEqual(response.status_code, 200)


    #     quests = Quest.objects.filter(title='test_quest_title')
    #     quest = quests[0]
    #     location = Location.objects.filter(quest=quest)
    #     location = locations[0]

    #     # print("Count: " + str(location.count()))

    #     self.assertTrue(quest.exists())
    #     self.assertEquals(quest.title, 'test_quest_title')
    #     self.assertEquals(location.title, 'test_location_title')
    #     self.assertEquals(location.clue, 'TestClue')
    #     self.assertEquals(location.lat, 10.10101)
    #     self.assertEquals(location.long, -11.10101)
    #     self.assertEquals(location.description, 'test_description')
    #     self.assertEquals(location.answer, 'test_answer')

    def test_QuestForm_valid_fields(self):
        # Create and validate Quest with QuestForm
        quest_data = {'title': 'test_quest', 'cache_type': 'Traditional'}
        quest_form = QuestForm(data=quest_data)
        self.assertTrue(quest_form.is_valid())

        # Add necessary fields and save object
        quest = quest_form.save(commit=False)
        quest.pub_date = timezone.now()

        quest.author = self.create_author()
        quest.save()
        
        # Validate that quest is in dB
        quest_from_db = Quest.objects.get(title=quest.title)
        self.assertEqual(quest_from_db.title, quest.title)
    
    def test_QuestForm_invalid_fields(self):
        # Create and validate Quest with QuestForm
        quest_data = {}
        quest_form = QuestForm(data=quest_data)
        self.assertFalse(quest_form.is_valid())


    def test_LocationForm_valid_fields(self):
        # Create a quest
        quest = self.create_quest()

        # Create and validate Location with LocationForm
        location_data = {'title': 'test_location_1', 'clue': 'test_clue_1', 'lat': 10.101, 'long': -11.101, 'quest': quest, 'description': 'test_description', 'answer': 'test_answer'}
        location_form = LocationForm(data=location_data)
        self.assertTrue(location_form.is_valid())

        # Add necessary fields and save object
        location = location_form.save(commit=False)
        location.quest_id = quest.id
        location_form.save()
        
        # Validate that location object is in dB
        location_from_db = Location.objects.get(title=location.title)
        self.assertEqual(location_from_db.title, location.title)
        self.assertEqual(location_from_db.clue, location.clue)
        self.assertEqual(location_from_db.lat, location.lat)
        self.assertEqual(location_from_db.long, location.long)
        self.assertEqual(location_from_db.description, location.description)
        self.assertEqual(location_from_db.answer, location.answer)

    def test_LocationForm_invalid_fields(self):
        # Create a quest
        quest = self.create_quest()

        # Create and validate Location with LocationForm with invalid fields
        location_data = {'title': 'test_location_1', 'clue': 'test_clue_1', 'lat': 'invalid lat', 'long': 'invalid long', 'quest': quest}
        location_form = LocationForm(data=location_data)
        self.assertFalse(location_form.is_valid())


#     # Change this to location form.
#     # def test_ChoiceFormSet_valid_fields(self):
#     #     # Create and validate Quest with QuestForm
#     #     quest_data = {'title': 'test_quest', }
#     #     quest_form = QuestForm(data=quest_data)
#     #     self.assertTrue(quest_form.is_valid())

#     #     # Add necessary fields before saving form
#     #     quest = quest_form.save(commit=False)
#     #     quest.pub_date = timezone.now()

#     #     quest.author = self.create_author()
#     #     quest.save()

#     #     # Create a ChoiceFormSet with the Quest and Location objects
#     #     location_data = [
#     #         {'title': 'test_location_1', 'clue': 'test_clue_1', 'lat': 10.101, 'long': -11.101},
#     #         # {'title': 'test_location_2', 'clue': 'test_clue_2', 'lat': 20.202, 'long': -22.202},
#     #     ]

#     #     # Create and populate form
#     #     location_formset = ChoiceFormSet(instance=quest, data=location_data)
#     #     for i in range(len(location_data)):
#     #         form = location_formset.forms[i]
#     #         form.data = location_data[i]

#     #     # for form in location_formset:
#     #     #     if form.is_valid():
#     #     #         form.instance.quest = quest  # Associate the location with the quest
#     #     #         form.save()

#     #     self.assertTrue(location_formset.is_valid())

#         # location_metas = location_formset.save(commit=False)
#         # for meta in location_metas:
#         #     meta.quest = self.object
#         #     meta.save()
#         # choice_formset.save()

#         # # Verify that the Quest and Location objects were created
#         # self.assertEqual(Quest.objects.count(), 1)
#         # self.assertEqual(Location.objects.count(), 2)

# # '''
# # Write test that will:
# # - Validate the data in the models.
# # - Check that people can't play or interact with not approved quests.
# # - Testing Forms
# #     csrf_client = Client(enforce_csrf_checks=True)  //Enforce CSRF Checking.

# # '''