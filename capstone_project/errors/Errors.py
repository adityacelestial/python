class UserNotFoundError(Exception):
    pass

class DuplicateUserError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class LoanNotFoundError(Exception):
    pass

class MaxPendingLoansError(Exception):
    pass

class InvalidLoanReviewError(Exception):
    pass
