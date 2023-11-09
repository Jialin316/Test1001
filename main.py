import qcm
import random

def get_good_bad_answers(user_answers:list, correct_answers:list):
    """rreturn le nombre de réponses correct et mauvaise de l'utilisateur

    Args:
        user_answers (list, obligatoire): Liste des numéros (int) des réponses de l'utilisateur. Defaults to list.
        correct_answers (list, obligatoire): Listes des numéros (int) des bonnes réponses. Defaults to list.

    Returns:
        int: nombre de réponse correct et mauvaise
    """
    
    number_of_good_answer = 0
    number_of_bad_answer = 0
    for answer in user_answers:
        if answer in correct_answers:
            number_of_good_answer += 1
        else:
            number_of_bad_answer += 1
    
    return number_of_good_answer, number_of_bad_answer


def correction_sympa(user_answers:list, correct_answers:list, user_current_score:int):
    """ - +1 point par bonne réponse
        - Si tout mauvais 0 point
    
    Args:
        user_answers (list, obligatoire): Liste des numéros (int) des réponses de l'utilisateur. Defaults to list.
        correct_answers (list, obligatoire): Listes des numéros (int) des bonnes réponses. Defaults to list.
        user_current_score (int, obligatoire): Le score actuel de l'utilisateur
    """
    
    number_of_good_answer, number_of_bad_answer = get_good_bad_answers(user_answers, correct_answers)
    
    user_current_score += number_of_good_answer
    
    return user_current_score


def correction_severe(user_answers:list, correct_answers:list, user_current_score:int):
    """ - Si tout bon +1 point 
	    - Si au moins une mauvaise réponse +0 point
        - Si tout mauvais -1 point

    Args:
        user_answers (list, obligatoire): Liste des numéros (int) des réponses de l'utilisateur. Defaults to list.
        correct_answers (list, obligatoire): Listes des numéros (int) des bonnes réponses. Defaults to list.
        user_current_score (int, obligatoire): Le score actuel de l'utilisateur
    """
    
    number_of_good_answer, number_of_bad_answer = get_good_bad_answers(user_answers, correct_answers)
    
    if number_of_good_answer == len(correct_answers) and number_of_bad_answer == 0:
        user_current_score += 1
    elif number_of_good_answer == 0:
        user_current_score -= 1
    
    return user_current_score


def correction_adaptative(user_answers:list, correct_answers:list, user_current_score:int, number_of_answers:int):
    """Si on répond aléatoirement, on obtient environ 0 

    Args:
        user_answers (list, obligatoire): Liste des numéros (int) des réponses de l'utilisateur.
        correct_answers (list, obligatoire): Listes des numéros (int) des bonnes réponses.
        user_current_score (int, obligatoire): Le score actuel de l'utilisateur
        number_of_answers (int, obligatoire): Le nombre de réponse possible
    """
    
    number_of_good_answer, number_of_bad_answer = get_good_bad_answers(user_answers, correct_answers)
            
    if number_of_good_answer == len(correct_answers) and number_of_bad_answer == 0:
        user_current_score += 1
            
    elif number_of_good_answer == 0:
        user_current_score -= 1 / (number_of_answers-1)
    
    return user_current_score


def ask_qcm():
    # Demande le QCM
    filename = __file__.replace("main.py", "Liste des QCM")
    
    QCM = input("Souhaitez vous le QCM 1 ou 2: ")
    while QCM not in ("1", "2"):
        QCM = input("Choix incorrect, veuillez réessayer: ")
    if QCM == "1":
        filename += "\QCM.txt"
    elif QCM == "2":
        filename += "\QCM2.txt"
        
    return filename


def ask_correction():
    print("Veuillez choisir votre méthode de correction:")
    print("\t1 : Sympa")
    print("\t2 : Adaptative")
    print("\t3 : Sévère")
    choice = ""
    while choice not in ("1", "2", "3"):
        choice = input("Votre choix : ")
        if choice == "1":
            return "Sympa"
        elif choice == "2":
            return "Adaptative"
        elif choice == "3":
            return "Sévère"


def build_questionnaire(filename):
    questions = qcm.build_questionnaire(filename)
    
    # Randomise l'ordre des questions et des réponses
    random.shuffle(questions)
    for question in questions:
        random.shuffle(question[1])
    
    return questions


def QCM(questionnaire:list, correction:str):
    user_score = 1000
    total_score = 0
    
    # Print chaque question avec ses propositions de réponses et attends la réponse du user
    for q in range(len(questionnaire)):
        # Print la question
        print(f'\n\nQuestion {str(q+1)}: {questionnaire[q][0]}')
        # Print les propositions de réponses avec leur numéro
        correct_answers = []
        number_of_answers = len(questionnaire[q][1])
        for r in range(number_of_answers):
            print(f'\t{r+1} : {questionnaire[q][1][r][0]}')
            # Créer la liste des numéros des bonnes réponses
            if questionnaire[q][1][r][1]:
                correct_answers.append(str(r+1))
        
        # Demande les réponses du user
        #user_answers = str(random.randint(1, number_of_answers))
        user_answers = input("Entrez le numéro de la réponse (si plusieurs réponses, séparer les numéros par une virgule et sans espace)): ")
        
        # Trie les réponses
        user_answers = user_answers.split(",")
        
        # Vérifie si c'est bon
        if correction == "Sévère":
            total_score = len(questionnaire)
            user_score = correction_severe(user_answers, correct_answers, user_score)
            
        elif correction == "Adaptative":
            total_score = len(questionnaire)
            user_score = correction_adaptative(user_answers, correct_answers, user_score, number_of_answers)
            
        elif correction == "Sympa":
            total_score += len(correct_answers)
            user_score = correction_sympa(user_answers, correct_answers, user_score)
            
            
    # Print la note et une phrase qui dit les questions auxquelles le user a faux
    print(f"\nVotre score est de : {user_score}/{total_score}.")


filename = ask_qcm()
questionnaire = build_questionnaire(filename)
correction = ask_correction()

QCM(questionnaire, correction)

