from typing import Any
from django.views import generic
from .models import *
from .forms import *
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import json, logging
from django.forms.models import model_to_dict
from math import isclose


class IndexView(generic.ListView):
    template_name = "maps/index.html"

    def get_queryset(self):
        return None


class CreateView(generic.CreateView):
    form_class = QuestForm
    model = Quest
    template_name = "maps/create.html"
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['location_formset'] = ChoiceFormSet(prefix="location_set")
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        location_formset = ChoiceFormSet(self.request.POST)
        # print(self.request.POST)
        if form.is_valid() and location_formset.is_valid():
            print("Form is valid.")
            return self.form_valid(form, location_formset)
        else:
            print("Form is invalid.")
            print(form.errors)
            print(location_formset.errors)
            if len(location_formset.errors) > 0:messages.error(self.request, "One or more location fields left blank")
            return self.form_invalid(form, location_formset)
        
    def form_valid(self, form, location_formset):
        
        self.object = form.save(commit=False)
        self.object.pub_date = timezone.now()

        try:
            a = Author.objects.get(email=self.request.user.email)
        except:
            a = Author(name=self.request.user.username, email=self.request.user.email)

        a.quests_created += 1
        a.save()

        self.object.author = a  
        self.object.save()
       
        location_metas = location_formset.save(commit=False)
        if location_metas:
            for meta in location_metas:
                meta.quest = self.object
                meta.save()

            return redirect(reverse("maps:index"))
        else:
            messages.error(self.request, "Please provide at least one location by clicking on the map.")
            return self.form_invalid(form, location_formset)
    
    def form_invalid(self, form, location_formset):
        return self.render_to_response(self.get_context_data(form=form, location_formset=location_formset))

class ApproveView(generic.ListView):
    template_name = "maps/approve.html"
    context_object_name = "latest_quest_list"

    def get_queryset(self):
        return Quest.objects.filter(feedback='Pending approval.')
    
    @method_decorator(staff_member_required(login_url="home"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["pending_quests"] = 
    #     return context


# class DetailsView(generic.DetailView):
#     model = Quest
#     template_name = "maps/details.html"

#     def get_queryset(self):
#         return Quest.objects.filter(pub_date__lte=timezone.now())

class UpdateView(generic.UpdateView):
    model = Quest
    template_name = "maps/details.html"
    form_class = QuestUpdateForm

    def get_success_url(self):
        return reverse("maps:approve")
    
    def form_valid(self, form):
        feedback = form.cleaned_data['feedback']

        quest = self.get_object()
        quest.feedback = feedback
        if feedback == 'Quest Approved':
            quest.status = True
        quest.save()

        return super().form_valid(form)
    
    # Validate staff permission or redirect.
    @method_decorator(staff_member_required(login_url="home"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # Additional context.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        quest = context['object']
        locations = quest.location_set.all()

        context['locations_json'] = json.dumps([{
            'title': location.title,
            'clue': location.clue,
            'lat': float(location.lat),     # Convert Decimal to float because of JSON
            'long': float(location.long),
        } for location in locations])

        return context

    
    



# def respond(request, quest_id):
#     quest = get_object_or_404(Quest, pk=quest_id)


class SearchView(generic.ListView):
    Model = Quest
    template_name = "maps/search.html"
    context_object_name = 'quests'

    def get_queryset(self):
        return None
    
    # Additional context for JS?
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quests = Quest.objects.filter(feedback='Quest Approved')       # Only Approved Quests displayed.
        
        quests_data = []
        for quest in quests:
            locations = Location.objects.filter(quest=quest)

            quest_include_fields = ['title', 'author', 'likes', 'id', "cache_type"]
            quest_dict = model_to_dict(quest, fields=quest_include_fields)
            quest_dict["difficulty"] = round(float(quest.difficulty), 2)

            quest_dict['locations'] = [{
                'title': location.title,
                'description': location.description,
                'clue': location.clue,
                'lat': float(location.lat),
                'long': float(location.long),
            } for location in locations]

            quest_dict['author'] = {
                'name': quest.author.name,
                'email': quest.author.email,
            } 

            quests_data.append(quest_dict)

        context['quests_data_json'] = json.dumps(quests_data)

        # Cache Type Context
        context['CACHE_TYPE_CHOICES'] = Quest.CACHE_TYPE_CHOICES

        return context


class LeaderboardView(generic.ListView):
    template_name = "maps/leaderboard.html"
    context_object_name = "author_quests_created"

    def get_queryset(self):
        return Author.objects.order_by("-quests_created")[:10]
    
    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        approved_quests = Quest.objects.filter(feedback='Quest Approved')
        context["author_quests_complete"] = Author.objects.order_by("-quests_complete")[:10]
        context["popular_quests"] = approved_quests.order_by("-likes")[:10]
        context["difficult_quests"] = approved_quests.order_by("-difficulty")[:10]

        # Have to neatly do this for all players.
        players = Player.objects.all()

        context['players'] = [{
                'name': player.user.username,
                'total_quests_completed': player.completed_quests.all().count(),
        } for player in players]
        context['players'].sort(key=lambda x : x["total_quests_completed"], reverse=True) # sort based on quests completed
        context['players'] = context['players'][:10] # limit display to top 10 players

        return context


class QuestView(generic.ListView):
    template_name = "maps/quests.html"
    context_object_name = "my_quests"

    def get_queryset(self):
        return Quest.objects.filter(author__email=self.request.user.email)

    def get_context_data(self, **kwargs):
        context = super(QuestView, self).get_context_data(**kwargs)
        context["my_quests"] = Quest.objects.filter(author__email=self.request.user.email)

        players = Player.objects.filter(user=self.request.user)
        if players.exists():
            player = players.get()
            context["played_quests"] = player.completed_quests.all()
            context["liked_quests"] = player.liked_quests.all()
        else:
            context["played_quests"] = []
            context["liked_quests"] = []
        
        return context

class HomePageView(generic.base.TemplateView):
    template_name = "home/home.html"

class PlayView(generic.UpdateView):
    template_name = "maps/play.html"
    model = Quest
    context_object_name = "quest"
    form_class = LikesForm

    def get_success_url(self):
        return reverse("maps:leaderboard")
    
    def get_object(self, queryset=None):
        return Quest.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quest = context['object']
        locations = quest.location_set.all()
        context["difficulty_form"] = DifficultyForm

        context['locations_json'] = json.dumps([{
            'title': location.title,
            'clue': location.clue,
            'lat': float(location.lat),  # Convert Decimal to float because of JSON
            'long': float(location.long),
        } for location in locations])

        # Change button to "Play Again?" if Quest Completed.
        players = Player.objects.filter(user=self.request.user)
        if players.exists():
            player = players.get()
            current_quest = Quest.objects.get(pk=self.kwargs['pk'])
            
            if current_quest in player.liked_quests.all():
                context['liked_quest'] = True
            else:
                context['liked_quest'] = False

            if current_quest in player.rated_quests.all():
                context['rated_quest'] = True
            else:
                context['rated_quest'] = False
            
            if current_quest in player.completed_quests.all():
                context["completed_quest"] = True
            else:
                context["completed_quest"] = False
        else:
            context["completed_quest"] = False
            context["liked_quest"] = False
            context["rated_quest"] = False

        return context
    
    def form_valid(self, form):
        quest = self.get_object()
        player, created = Player.objects.get_or_create(user=self.request.user)
        if not 'difficulty' in form.fields:
            player.liked_quests.add(quest)
        else:
            player.rated_quests.add(quest)
        player.save()

        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()

        if "difficulty" in request.POST:
            self.object.save()
            form_class = DifficultyForm
        
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class GuessView(generic.FormView):
    template_name = "maps/guess.html"
    form_class = GuessForm
    model = Location
    context_object_name = "location"

    def get_location_by_locnum(self, quest, locnum):
        locations = quest.location_set.all()
        if 1 <= locnum <= len(locations):
            return locations[locnum - 1]
        return None

    def get_object(self):
        quest = Quest.objects.get(pk=self.kwargs['pk'])
        locations = quest.location_set.all()
        locnum = self.kwargs['locnum']
        return locations[locnum - 1]

    def get_success_url(self):
        if self.kwargs['locnum'] == len(Quest.objects.get(pk=self.kwargs['pk']).location_set.all()):
            # this is where we can note that the user has completed this quest
            return reverse("maps:play", kwargs={'pk':self.kwargs['pk']})

        locnum = self.kwargs['locnum'] + 1
        return reverse("maps:guess", kwargs={'pk':self.kwargs['pk'], 'locnum':locnum})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        answer = str.lower(form.cleaned_data['answer'])
        location = self.get_object()
        expected_answer = str.lower(location.answer)
        if answer == expected_answer:
            # Add completed location to an author.
            # try:
            #     player = self.request.user.player
            # except:
            #     player = Player(self.request.user)
            player, created = Player.objects.get_or_create(user=self.request.user)
            player.completed_locations.add(location)
            player.save()
            if self.all_locations_completed(player):
                player.completed_quests.add(Quest.objects.get(pk=self.kwargs['pk']))
                player.save()

            # author = Author.objects.get(email=self.request.user.email)
            # print(self.object.author.email)
            # print(Author.objects.get(email=self.request.user.email).email)

            return super().form_valid(form)
        else:
            messages.error(self.request, "Incorrect guess, please try again.")          #https://docs.djangoproject.com/en/4.2/ref/contrib/messages/
            return super().form_invalid(form)
        
        # lat = form.cleaned_data['lat']
        # long = form.cleaned_data['long']

        # location = self.get_object()
        # if isclose(lat, location.lat, rel_tol=0.001, abs_tol=0):
        #     if isclose(long, location.long, rel_tol=0.001, abs_tol=0):
        #         return super().form_valid(form)

    def all_locations_completed(self, player):
        quest = Quest.objects.get(pk=self.kwargs['pk'])
        locations = quest.location_set.all()
        completed_locations = player.completed_locations.filter(quest=quest)
        if set(locations) == set(completed_locations):
            print("All Locations have been completed!")
            return True
        else:
            return False


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quest = Quest.objects.get(pk=self.kwargs['pk'])
        locations = quest.location_set.all()

        # Context for HTML
        locnum = int(self.kwargs['locnum'])
        current_location = self.get_location_by_locnum(quest, locnum)
        context['curr_location'] = current_location

        context['locations_json'] = json.dumps([{
            # 'title': location.title,
            # 'clue': location.clue,
            'lat': float(location.lat),  # Convert Decimal to float because of JSON
            'long': float(location.long),
            'pk': location.pk,
        } for location in locations])

        context['curr_locnum_json'] = json.dumps({'locnum': self.kwargs['locnum']})     # The pk of the current URL (last num in URL)

        return context
    
class AboutPageView(generic.ListView):
    template_name = "home/about.html"

    def get_queryset(self):
        return None