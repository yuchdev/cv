import argparse
import datetime
import sys
import json

from code_generation.html.html_file import HtmlFile
from code_generation.html.html_element import HtmlElement


def header(data, html):
    html(f'<!doctype HTML>')
    with html.block('head', lang='en'):
        HtmlElement(
            name='meta', self_closing=True, charset='utf-8'
        ).render_to_string(html)
        HtmlElement(
            name='meta', self_closing=True, viewport='width=device-width, initial-scale=1'
        ).render_to_string(html)
        HtmlElement(
            name='meta', self_closing=True, attributes={"http-equiv": "default-style", "content": "cv.css"}
        ).render_to_string(html)
        HtmlElement(
            name='link', self_closing=True, rel='stylesheet', href='cv.css'
        ).render_to_string(html)

        HtmlElement(name='title').render_to_string(
            html, content=f"{data['Personal Information']['Name']}")


def personal_details(html, data):
    # Personal details
    with html.block('table', attributes={'class': 'personal-details'}):
        html(f'<tr><th>Name</th><td>{data["Personal Information"]["Name"]}</td></tr>')
        html(f'<tr><th>Birthdate</th><td>{data["Personal Information"]["Birthdate"]}</td></tr>')
        html(f'<tr><th>E-mail</th><td>{data["Personal Information"]["E-mail"]}</td></tr>')
        with html.block('tr'):
            html('<th>Phone</th>')
            with html.block('td'):
                with html.block('ul'):
                    for phone in data["Personal Information"]["Phone"]:
                        html(f'<li>{phone}</li>')
        html(
            f'<tr><th>Current location</th><td>{data["Personal Information"]["Current location"]}</td></tr>')


def overview(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Overview')
        html(f'<p>{data["Overview"]}</p>')


def professional_skills(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Professional Skills')
        with html.block('ul', attributes={'class': 'skills'}):
            for skill, subskills in data['Professional skills'].items():
                with html.block('li', attributes={'class': 'skill'}):
                    html(skill)
                    with html.block('ul', attributes={'class': 'subskills'}):
                        for subskill in subskills:
                            html(f'<li class="subskill">{subskill}</li>')


def work_experience(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Experience')
        for key, experience in data['Employment history'].items():
            with html.block('div', attributes={'class': 'job'}):
                with html.block('h3'):
                    html(f'{experience["Period"]}')
                with html.block('h4'):
                    html(f'{experience["Name"]} - {experience["Brief"]}')

                job_description_subkeys = [
                    "Position",
                    "Description",
                    "Projects",
                    "Programming languages, products and technologies"]
                # Generate a table for job description key-value pairs
                job_description(experience, html, job_description_subkeys)


def job_description(experience, html, job_description_subkeys):
    with html.block('table', attributes={'class': 'job-description'}):
        # Iterate over each key
        for subkey in job_description_subkeys:
            # Handle Projects subkey separately
            with html.block('tr'):
                if subkey == "Projects":
                    # Start a nested table for projects
                    html(f'<th>{subkey}:</th>')
                    with html.block('td'):
                        with html.block('dl', attributes={'class': 'projects'}):
                            for project_name, project_desc in experience[subkey].items():
                                # Add each project as a nested row in the table
                                with html.block('dl'):
                                    html(f'<dt>{project_name}</dt>')
                                    html(f'<dd>{project_desc}</dd>')
                else:
                    # Add all other subkeys as a regular row in the table
                    with html.block('tr'):
                        html(f'<th>{subkey}:</th>')
                        html(f'<td>{experience[subkey]}</td>')


def education(data, html):
    with html.block('div', attributes={'class': 'section'}):
        with html.block('h2'):
            html('Education')
        for edu in data['Education']:
            with html.block('div', attributes={'class': 'education'}):
                with html.block('h3'):
                    html(edu['Institution'])
                with html.block('h3'):
                    html(edu['Degree'])
                with html.block('h4'):
                    html(f'{edu["Graduation"]}')
                with html.block('p'):
                    html(f'{edu["Achievements"]}')


def footer(data, html):
    year = datetime.datetime.now().year
    with html.block('footer'):
        html(
            f'{data["Personal Information"]["Name"]} &copy; {year}'
        )


def generate_cv_from_json(json_file_path: str, html_file_path: str):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    html = HtmlFile(html_file_path)

    with html.block('html'):
        header(data, html)
        with html.block('body'):
            with html.block('div', id='container'):
                with html.block('div', id='header'):
                    html(f'<h1 class=cv-header>{data["Personal Information"]["Name"]}</h1>')
                with html.block('div', id='content'):
                    personal_details(html, data)
                    overview(data, html)
                    professional_skills(data, html)
                    work_experience(data, html)
                    education(data, html)
        footer(data, html)


def main():
    parser = argparse.ArgumentParser(description='Command-line params')
    parser.add_argument('--json-cv',
                        help='JSON document to convert to HTML CV',
                        default="cv.json",
                        required=False)
    parser.add_argument('--html-cv',
                        help='HTML CV output file',
                        default="cv.html",
                        required=False)
    args = parser.parse_args()
    generate_cv_from_json(args.json_cv, args.html_cv)
    return 0


if __name__ == '__main__':
    sys.exit(main())
