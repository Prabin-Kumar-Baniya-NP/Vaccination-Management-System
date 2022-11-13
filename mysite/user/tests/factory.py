import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.User"

    email = factory.faker.Faker("email")
    password = factory.PostGenerationMethodCall(
        'set_password', raw_password='abcde@12345')
    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    date_of_birth = factory.faker.Faker("date")
    gender = factory.fuzzy.FuzzyChoice(['M', 'F'])
    blood_group = factory.fuzzy.FuzzyChoice(["A+", "B+", "O+" "AB+"])
    identity_document_type = factory.fuzzy.FuzzyChoice(
        ["Passport", "Voter ID", "Citizenship Number"])
    identity_document_number = factory.fuzzy.FuzzyInteger(100, 100000)
    photo = factory.django.ImageField(color="blue")
    is_email_verified = True
    is_active = True
    is_staff = False
    is_superuser = False
