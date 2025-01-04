def calculate_final_percentage(
    bank_percentage: float, iva: float, with_iva: bool
) -> float:
    iva_percentage = bank_percentage * iva if with_iva else 0
    return bank_percentage + iva_percentage


def calculate_selling_price(
    cost: float, desired_margin: float, final_percentage: float
) -> float:
    if (1 - desired_margin - (final_percentage / 100)) <= 0:
        return -1
    return cost / (1 - desired_margin - (final_percentage / 100))
