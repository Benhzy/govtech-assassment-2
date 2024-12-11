
def meets_criterion(applicant, criterion):
    ctype = criterion.criterion_type
    cvalue = criterion.criterion_value
    person = applicant.person

    print(ctype, cvalue)

    if ctype == 'age':
        print(person.age)
        operator = cvalue[0]
        threshold = int(cvalue[1:])
        if operator == '>':
            return person.age > threshold
        elif operator == '<':
            return person.age < threshold
        return False

    elif ctype == 'marital_status':
        return person.marital_status == cvalue

    elif ctype == 'sex':
        return person.sex == cvalue
            
    elif ctype == 'employment_status':
        return person.employment_status == cvalue

    elif ctype == 'current_education':
        return person.current_education == cvalue

    elif ctype == 'monthly_income':
        operator = cvalue[0]
        threshold = float(cvalue[1:])
        applicant_income = person.monthly_income if person.monthly_income is not None else 0.0
        if operator == '>':
            return applicant_income > threshold
        elif operator == '<':
            return applicant_income < threshold
        return False

    elif ctype == 'completed_national_service':
        required = (cvalue.lower() == 'true')
        return person.completed_national_service == required
    
    elif ctype == 'disability':
        required = (cvalue.lower() == 'true')
        return person.disability == required
    
    elif ctype == 'household_member_relationship':
        for member in applicant.household_members.all():
            if member.relationship_to_applicant == 'Child':
                return True
        return False

    elif ctype == 'household_member_age':
        print(person.age)
        operator = cvalue[0]
        threshold = int(cvalue[1:])
        for member in applicant.household_members.all():
            if member.relationship_to_applicant == 'Child':
                if operator == '>':
                    return person.age > threshold
                elif operator == '<':
                    return person.age < threshold
        return False
    
    elif ctype == 'household_member_education':
        for member in applicant.household_members.all():
            if member.relationship_to_applicant == 'Child'and member.person.current_education == cvalue:
                return True
        return False

    else:
        raise ValueError(f"Unknown criterion type: '{ctype}' is not in the system.")
