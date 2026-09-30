import uvicorn
 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HCI Mini Review App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = [{
                "id": 0,
                "q": "Is Fitts' Law an example of a predictive model or a descriptive model?",
                "a": "Predictive model"
                },
             {
                "id": 1,
                "q": "Does this course focus more on genius design, systems design, or user-centered design?",
                "a": "User-centered design"
                },
             {
                "id": 2,
                "q": "What is the main goal of the ideation phase of iterative design?",
                "a": "Generating as many possible design solutions as possible"
                }
            ]

class QuestionRequest(BaseModel):
    question: str
    answer: str

@app.get("/questions")
def get_questions():
    return questions

@app.post("/add")
def add_question(req: QuestionRequest):
    questions.append({ 
        "id": len(questions),
        "q": req.question,
        "a": req.answer
    })

@app.delete("/delete/{id}")
def delete_question(id: int) -> None:
    """Removes a question with the given id from the in-memory database.
    
    Args:
        id: The id corresponding to the question to delete.
    
    Raises:
        HTTPException: If the given question id does not exist in the in-memory database.
    """
    for x in questions:
        if x["id"] == id:
            questions.remove(x)
            return
    raise HTTPException(status_code=404, detail="Question with ID {id} not found")

@app.put("/update/{id}")
def update_question(id: int, req: QuestionRequest) -> None:
    """Update the contents of a question with given question request.
    
    Args:
        id: The id corresponding to the question to update.
        req: The contents of to update the question with.

    Raises: HTTPException: If the given question id does not exist in the in-memory database.
    """
    for x in questions:
        if x["id"] == id:
            x["q"] = req.question
            x["a"] = req.answer
            return
    raise HTTPException(status_code=404, detail="Question with ID {id} not found")

if __name__=="__main__":
    uvicorn.run(app, port=8005)