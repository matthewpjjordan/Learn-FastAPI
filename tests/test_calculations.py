import pytest
from app.calc import add, sub, mul, div, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(5, 3, 8), (3, 11, 14), (51, 9, 60)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_sub():
    assert sub(5, 3) == 2


def test_mul():
    assert mul(5, 3) == 15


def test_div():
    assert div(6, 3) == 2


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40


def test_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize(
    "depostied, withdrew, expected", [(200, 100, 100), (50, 10, 40)]
)
def test_bank_transaction(zero_bank_account, depostied, withdrew, expected):
    zero_bank_account.deposit(depostied)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(60)
