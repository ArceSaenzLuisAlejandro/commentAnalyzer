import os
import openai
import pandas as pd

# API Key
openai.api_key = "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"

examples_dataset = [
            ["No pude alcanzar mis objetivos de publicaciones ya que no cuento con un laboratorio con la instrumentacion adecuada para realizar la experimentacion que ayude a generar los resultados esperados. Por el lado de la ecoa, los alumnos no mostraron una buena actitud que ayudara al buen desarrollo de la clase."
            ,"Justificable"],
            ["No pude alcanzar mis objetivos de publicaciones ya que tengo otro trabajo, ademas que no me han podido dar un lugar de trabajo en la escuela. Por el lado de la academia, los alumnos no mostraron una buena actitud para aprender, por eso el bajo resultado.."
            ,"No justificable"]
        ]

response = openai.Classification.create(
        # Aquí tengo duda, cuál es el search y cuál es el model
        search_model="davinci",
        model="davinci",
        temperature=0.9,
        max_examples=526,
        examples=examples_dataset,
        query="No alcance mis objetivos de publicaciones porque estuve enfocado solamente en dar clases.",
        labels=["Justificable", "No justificable"],
    )


