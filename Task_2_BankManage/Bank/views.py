from django.shortcuts import render
from Bank.models import Person
from django.db.transaction import atomic
from decimal import Decimal
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def index(request):
    if request.method == "GET":
        return render(request=request, template_name='Bank/index.html')
    elif request.method == "POST":
        if request.path.replace("/", "") == "calculate":
            try:
                input_commands = [command.strip("\r") for command in request.POST.get("input_command").split("\n") if not command.isspace() and command != ""]
                output_commands = []
                if len(input_commands) <= 20:
                    for command in input_commands:
                        command, *args = command.split()
                        output_commands.append(globals()[command.lower()](*args))
                else:
                    output_commands.append("The maximum number of commands entered at a time must not exceed 20")
            except:
                output_commands.append("Incorrect command!")
            buffer_command = dict([("input_commands", input_commands), ("output_commands", output_commands)])
            return render(request=request, template_name='Bank/index.html', context={'buffer_command': buffer_command})
        elif request.path.replace("/", "") == "clear":
            return render(request=request, template_name='Bank/index.html')


@atomic
def deposit(name, sum):
    try:
        person = Person.objects.get(name=name)
        person.money += Decimal(sum)
        person.save()
        return f"{sum} was credited to client {name} account" \
               f"\nThe balance is equal to: {person.money}"
    except Person.DoesNotExist:
        Person.objects.create(name=name, money=Decimal(sum))
        return f"{name} was not a client, he was opened an account and credited {sum}" \
               f"\nThe balance is equal to: {sum}"


@atomic
def withdraw(name, sum):
    try:
        person = Person.objects.get(name=name)
        person.money -= Decimal(sum)
        person.save()
        return f"{sum} was debited from the client's account {name}" \
               f"\nThe balance is equal to: {person.money}"
    except Person.DoesNotExist:
        Person.objects.create(name=name, money=-Decimal(sum))
        return f"{name} was not a customer, but an account was opened for him. The balance is equal to: -{sum}"


@atomic
def balance(name=None):
    if name is None:
        all_persons = str()
        for person in Person.objects.all():
            all_persons += f"{person.name} {person.money} \n"
        if all_persons != "":
            return all_persons.rstrip('\n')
        else:
            return "There are no clients in the database!"
    else:
        try:
            person = Person.objects.get(name=name)
            return f"The client's balance {person.name} is equal to: {person.money}"
        except Person.DoesNotExist:
            return f"{name} - NO CLIENT"


@atomic
def transfer(name_from, name_to, sum):
    try:
        name_from = Person.objects.get(name=name_from)
        sum = int(sum)
        if name_from.money > sum > 0:
            try:
                name_to = Person.objects.get(name=name_to)
                name_from.money = withdraw(name_from, sum)
                name_to.money = deposit(name_to, sum)
                return f"The transfer from [{name_from}] to [{name_to}] in the amount of {sum} was successfully completed!"
            except Person.DoesNotExist:
                name_from.money = withdraw(name_from, sum)
                Person.objects.create(name=name_to, money=sum)
                return f"{name_to}'s client's account was opened and {sum} of {name_from}'s money was transferred to him" \
                       f"\nThe balance is equal to: {sum}"
        else:
            return "The command was not executed for the following reason: " \
                   "Insufficient loans or the transfer amount is negative or equal to 0"
    except Person.DoesNotExist:
        return "The sender's account was not found in the database"


@atomic
def income(percent):
    for person in Person.objects.all().filter(money__gte=0):
        person.money += int(person.money / 100 * int(percent))
        person.save()
    return f"Customers with a positive account balance were credited with {percent}% of the invoice amount."
