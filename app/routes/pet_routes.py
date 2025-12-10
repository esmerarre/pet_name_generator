from flask import Blueprint, request, abort, make_response
from ..db import db
from ..models.pet import Pet
from google import genai

client = genai.Client()

bp = Blueprint("pets", __name__, url_prefix="/pets")

@bp.post("")
def create_pet():
    pass

@bp.get("")
def get_pets():
    pet_query = db.select(Pet)

    pets = db.session.scalars(pet_query)
    response = []

    for pet in pets:
        response.append(pet.to_dict())

    return response

@bp.get("/<pet_id>")
def get_single_pet(pet_id):
    pet = validate_model(Pet,pet_id)
    return pet.to_dict()

def validate_model(cls,id):
    try:
        id = int(id)
    except:
        response =  response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if model:
        return model

    response = {"message": f"{cls.__name__} {id} not found"}
    abort(make_response(response, 404))

#Nadia suggestion
def generate_pet_name(species, color, personality):
    prompt = f"""
    You are helping choose a name for a pet.

    Species: {species}
    Color: {color}
    Personality: {personality}

    Generate ONE unique, cute, memorable name that fits this pet.
    Return ONLY the name, with no explanations, no punctuation, and no quotes.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip().strip(" \"'.,")