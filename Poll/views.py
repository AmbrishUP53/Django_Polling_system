from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from .models import Polls , Candidate , Vote
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import transaction

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')



@login_required
def home(request):
    polls = Polls.objects.all().order_by('start_time')

    now = timezone.now()

    for poll in polls:
        if now < poll.start_time:
            poll.status = "Not Started"
        elif now > poll.end_time:
            poll.status = "Ended"
        else:
            poll.status = "Active"

    return render(request, 'home.html', {
        'polls': polls
    })


# @login_required
# def vote(request, poll_id):
#     poll = get_object_or_404(Polls, id=poll_id)

#     now = timezone.now()

#     # Poll has not started
#     if now < poll.start_time:
#         return render(request, 'vote.html', {
#             'poll': poll,
#             'status': 'not_started'
#         })

#     # Poll has ended
#     if now > poll.end_time:
#         return redirect('results', poll_id=poll.id)

#     # Check if user has already voted
#     already_voted = Vote.objects.filter(
#         user=request.user,
#         poll=poll
#     ).exists()

#     if already_voted:
#         return render(request, 'vote.html', {
#             'poll': poll,
#             'status': 'already_voted'
#         })

#     # Handle vote submission
#     if request.method == 'POST':

#         candidate_id = request.POST.get('candidate')

#         if not candidate_id:
#             return render(request, 'vote.html', {
#                 'poll': poll,
#                 'status': 'active',
#                 'error': 'Please select a candidate.'
#             })

#         # Make sure candidate belongs to this poll
#         candidate = get_object_or_404(
#             Candidate,
#             id=candidate_id,
#             Polls=poll
#         )

#     with transaction.atomic():
#         # Save vote
#         Vote.objects.create(
#             user=request.user,
#             poll=poll,
#             candidate=candidate
#         )

#         return render(request, 'vote.html', {
#             'poll': poll,
#             'status': 'success',
#             'candidate': candidate
#         })

#     # Show voting form
#     return render(request, 'vote.html', {
#         'poll': poll,
#         'status': 'active'
#     })

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Polls, id=poll_id)
    candidates = poll.candidates.all()
    now = timezone.now()

    # Poll has not started
    if now < poll.start_time:
        return render(request, 'vote.html', {
            'poll': poll,
            'candidates': candidates,
            'status': 'not_started'
        })

    # Poll has ended
    if now > poll.end_time:
        return redirect('results', poll_id=poll.id)

    # Check if user has already voted
    already_voted = Vote.objects.filter(
        user=request.user,
        poll=poll
    ).exists()

    if already_voted:
        return render(request, 'vote.html', {
            'poll': poll,
            'candidates': candidates,
            'status': 'already_voted'
        })

    # Handle vote submission
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')

        if not candidate_id:
            return render(request, 'vote.html', {
                'poll': poll,
                'candidates': candidates,
                'status': 'active',
                'error': 'Please select a candidate.'
            })

        # Make sure candidate belongs to this poll
        candidate = get_object_or_404(
            Candidate,
            id=candidate_id,
            Polls=poll
        )

        # Save vote
        with transaction.atomic():
            Vote.objects.create(
                user=request.user,
                poll=poll,
                candidate=candidate
            )

        return render(request, 'vote.html', {
            'poll': poll,
            'candidates': candidates,
            'status': 'success',
            'candidate': candidate
        })

    # Show voting form
    return render(request, 'vote.html', {
        'poll': poll,
        'candidates': candidates,
        'status': 'active'
    })

@login_required
def results(request, poll_id):
    poll = get_object_or_404(Polls, id=poll_id)

    now = timezone.now()

    # Results are available only after poll ends
    if now <= poll.end_time:
        return redirect('home')

    candidates = poll.candidates.annotate(
        vote_count=Count('vote')
    )

    total_votes = Vote.objects.filter(
        poll=poll
    ).count()

    for candidate in candidates:
        if total_votes > 0:
            candidate.percentage = round(
                (candidate.vote_count / total_votes) * 100,
                2
            )
        else:
            candidate.percentage = 0

    return render(request, 'results.html', {
        'poll': poll,
        'candidates': candidates,
        'total_votes': total_votes
    })