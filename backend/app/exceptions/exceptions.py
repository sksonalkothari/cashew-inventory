class BaseAppException(Exception):
    def __init__(self, message: str, status_code: int = 400, field: str = "general"):
        self.message = message
        self.status_code = status_code
        self.field = field
        super().__init__(self.message)

# Domain-specific exceptions
class AuthError(BaseAppException): pass
class UserError(BaseAppException): pass
class GradeError(BaseAppException): pass
class BatchSummaryError(BaseAppException): pass
class BatchError(BaseAppException): pass
class PurchaseError(BaseAppException): pass
class BoilingError(BaseAppException): pass
class DryingError(BaseAppException): pass
class HumidifyingError(BaseAppException): pass
class PeelingBeforeDryingError(BaseAppException): pass
class PeelingAfterDryingError(BaseAppException): pass
class HuskReturnError(BaseAppException): pass
class ProductionError(BaseAppException): pass
class RcnSalesError(BaseAppException): pass
class HuskRejectionSalesError(BaseAppException): pass
class CashewKernelSalesError(BaseAppException): pass
class CashewShellSalesError(BaseAppException): pass
class ReportError(BaseAppException): pass