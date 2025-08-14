from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db, Candidate, Vote
from forms import VoteForm, CandidateForm

# HTML routes
main = Blueprint("main", __name__)

@main.route("/")
def index():
    candidates = Candidate.query.all()
    return render_template("index.html", candidates=candidates)

@main.route("/vote", methods=["GET", "POST"])
def vote_page():
    vote_form = VoteForm()
    vote_form.candidate_id.choices = [(c.id, f"{c.name} ({c.party})") for c in Candidate.query.all()]

    if vote_form.validate_on_submit():
        if Vote.query.filter_by(voter_name=vote_form.voter_name.data).first():
            flash("You have already voted!", "danger")
        else:
            vote = Vote(voter_name=vote_form.voter_name.data, candidate_id=vote_form.candidate_id.data)
            db.session.add(vote)
            db.session.commit()
            flash("Vote cast successfully!", "success")
        return redirect(url_for("main.index"))

    candidate_form = CandidateForm()
    return render_template("vote.html", vote_form=vote_form, candidate_form=candidate_form)

@main.route("/add_candidate", methods=["POST"])
def add_candidate_page():
    candidate_form = CandidateForm()
    if candidate_form.validate_on_submit():
        candidate = Candidate(name=candidate_form.name.data, party=candidate_form.party.data)
        db.session.add(candidate)
        db.session.commit()
        flash("Candidate added successfully!", "success")
    else:
        flash("Failed to add candidate. Check input.", "danger")
    return redirect(url_for("main.vote_page"))

@main.route("/results")
def results_page():
    candidates = Candidate.query.all()
    results = {c.name: len(c.votes) for c in candidates}
    return render_template("results.html", results=results)

# API routes for Postman
api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/candidates", methods=["GET"])
def api_get_candidates():
    candidates = Candidate.query.all()
    return jsonify([{"id": c.id, "name": c.name, "party": c.party} for c in candidates])

@api.route("/vote", methods=["POST"])
def api_add_vote():
    data = request.json
    if Vote.query.filter_by(voter_name=data["voter_name"]).first():
        return jsonify({"message": "You have already voted!"}), 400
    vote = Vote(voter_name=data["voter_name"], candidate_id=data["candidate_id"])
    db.session.add(vote)
    db.session.commit()
    return jsonify({"message": "Vote cast successfully!"}), 201

@api.route("/results", methods=["GET"])
def api_results():
    candidates = Candidate.query.all()
    return jsonify({c.name: len(c.votes) for c in candidates})
