from llmproxy import generate

if __name__ == '__main__':
    information = """
    Combined-Degrees Programs
    Combined Five-Year Arts and Sciences/Engineering Program
    For most students entering college, the choice between liberal arts and engineering is a clear-cut matter. For some
    students, however, the choice is quite difficult. For the latter, both the professional flavor and occupational orientation of
    the engineering programs, on the one hand, and the variety of course selection in the liberal arts curriculum, on the
    other, have strong appeal. At Tufts, it is possible for students to secure the advantages of both types of education under
    the combined five-year program.
    With a normal course load in each of 10 semesters, it might be possible for students to complete the degree requirements in
    both engineering and arts and sciences. The five-year program includes two fields of major concentration, one in arts and
    sciences and one in engineering. The plan has particular appeal for engineering students who wish to secure a more liberal
    arts education than is possible in a four-year engineering curriculum and for arts and sciences students who desire a strong
    technological background.
    Two degrees are awarded on completion of the program. Both degrees are awarded only on completion of the entire
    program; a student may not receive one degree earlier, even if the requirements for that degree have been met. Students
    who start a five-year program, but decide within two years not to continue, may complete the degree requirements for
    either engineering or arts and sciences in the usual period of four years.
    Students may apply for and be admitted to the combined five-year program only after entrance to Tufts. Because the
    program requires careful planning, students are encouraged to apply as early as possible. Five-year students are required to
    confer with their faculty advisors at the beginning of each semester to make certain that the courses that have been
    selected constitute a proper program. Five-year students must complete a minimum of forty-six courses and fulfill the
    foundation, distribution, and concentration requirements of both engineering and arts and sciences. Within the School of
    Engineering, the B.S. degree may not be used as part of this program, except for the engineering psychology (human
    factors) program.

    Combined Degree BFA + BA/BS Program with SMFA at Tufts
    Students in the combined degree BFA + BA/BS program will be in full-time residence for a minimum of 8 semesters; will
    complete a minimum of 85 credits of non-studio coursework and 76 credits of studio art coursework. The non-studio
    distribution requirements for the BFA are satisfied by students completing 15 credits in art history, in addition to the
    distribution, foundation, and concentration requirements for their BA or BS degree, with the exception of their Arts
    Distribution requirement, which is satisfied by studio coursework taken towards their BFA degree. There are instances
    where students may use courses to satisfy multiple requirements in close consultation with their advising team. Normally,
    the majority of the non-studio work is taken on the Tufts Medford/Somerville campus, and most of the studio art courses
    are taken at the SMFA. Please reference the General Undergraduate Information, the School of Arts and Sciences (BA/BS)
    degree requirements and the School of Arts and Sciences (BFA) sections for the specific graduation requirements for the
    BFA degree and the BA/BS degree.
    Students who move from the combined degree program to the BA/BS program may still count up to 6 credits of studio
    coursework, graded Credit/No Credit, to satisfy the Arts distribution requirement; this is an exception to the requirement that
    distribution courses be taken for a letter grade.
    Students transferring from outside institutions entering the Combined Degree BFA & BA/BS program must spend a minimum
    of four full-time semesters at Tufts or on Tufts Programs Abroad and must complete at least half the credits required for each
    degree at Tufts or on Tufts Programs Abroad. Students are able to transfer up to 43 credits of non-studio coursework towards
    the BA/BS portion of their degree and 38 credits of studio coursework towards the BFA portion of their degree.

    Pass/Fail Option
    Within the limits stated below, students may elect to have their grades in certain courses recorded simply as pass or fail.
    The purpose of this option is to encourage students to extend their academic interests; it is not designed as a safety
    valve to permit students to carry unrealistic academic loads. The instructor is not aware if the student has elected to take
    the course with pass/fail grading. A student will be graded as usual throughout the course, with final grades transcribed
    by the registrar into pass (if D- or better) or fail. A pass does not affect the grade point average; a failing grade is
    averaged into the grade point average. A course that has been taken using the pass/fail grading option and for which the
    student earned a pass may not be repeated for credit. If a class that has been taken pass/fail is later needed for a major
    requirement that was not anticipated, the student may submit a petition request to his or her Advising Dean to have the
    originally assigned grade restored.

    Distribution Requirements
    The faculty holds that a student enrolled in any program leading to a liberal arts degree must demonstrate a
    reasonable acquaintance with each of the following five areas of inquiry: the humanities, the arts, the social
    sciences, the natural sciences, and the mathematical sciences.
    • A student must take at least six semester hours in each area.
    • No more than 3 courses, of any number of semester hours, may be from the same department or program.
    • At least 3 semester hours in each area must come from credits earned after matriculation.
    • No single course may be used in more than one distribution area.
    """

    system_prompt = f"""
        You are an academic advisor responding to student emails based on provided materials. 
        Your response should follow this format:
        
        ---
        Hi {{student_name}},  
        Thank you for reaching out!
        
        {{Reply}} 
        
        If you have any questions, please let me know.  
        
        Best,  
        Academic Advisor, Megan
        ---
        
        Guidelines:
        1. You are the advising team for this student. DO NOT in any where of the email to ask the student to confirm,
            discuss, or consult with their advising team. You ARE their advising team!
        2. Do not repeat the question back to the student.
        3. If no conclusion could be drawn from the information, say so and highlight that you will get back to the student
        4. If more information from the student is needed to form a conclusion, ask the student for clarification.
            List the possible conclusions depending on student responses.
        5. If the Reply is too long, break it down into paragraphs. Make sure that the transition is smooth and each
            paragraph talks about different ideas.
        6. Maintain a professional yet approachable tone and make the sentences clear and concise. If the student 
            expresses stress or concern, respond with empathy. 
        7. Ensure the response is formal but not excessively rigid.  
        8. Only use information from the provided materials — avoid assumptions.  
    
        Reference Information:  
        {information}
    """

    student_query = (
        "Hi, I am in the Dual degree program but I am dropping my SMFA degree. "
        "I am graduating in May and I just remembered that all studio classes I took "
        "are all pass/fail rather than having a letter grade, which I think is the requirement "
        "for a BA degree. Is this a problem for my graduation? Thanks! To life, Katie"
    )

    response = generate(
        model='4o-mini',
        system=system_prompt,
        query=student_query,
        temperature=0.0,
        lastk=0,
        session_id='GenericSession'
    )

    print(response)