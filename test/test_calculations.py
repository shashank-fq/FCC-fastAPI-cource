import pytest

from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divde():
    assert divide(20, 5) == 4


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    # bank_account = BankAccount(60)
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_intrest(bank_account):
    # bank_account = BankAccount(60)
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("num1, num2, expected", [
    (300, 200, 100),
    (72, 40, 32),
    (12, 4, 8),
])

def test_bank_transaction(zero_bank_account, num1, num2, expected):
    zero_bank_account.deposit(num1)
    zero_bank_account.withdraw(num2)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)