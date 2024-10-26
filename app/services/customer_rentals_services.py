import datetime
import logging
from typing import Any, Dict, List

from app.ai.gpt.services import query_gpt_model
from app.queries import create_query, retrieve_query
from app.schema import CustomerRentalsSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DiscountCalculator:
    def __init__(self, prompt: str):
        """Initialize the DiscountCalculator with the given prompt.

        Args:
            prompt (str): The user prompt containing customer information for discount calculation.
        """
        self.prompt = prompt

    @classmethod
    def _system_message_instructions(cls) -> str:
        """Generate system message instructions for the LLM to calculate discounts.

        The instructions outline the discount criteria based on customer attributes
        such as age, disability status, and pre-existing medical conditions.

        Returns:
            str: A formatted string containing instructions for the LLM.
        """
        return """You are a discount calculator for a service. Determine the highest applicable discount based on the following criteria:

        Age Discounts:
        - 0-12 years: 20% discount
        - 13-18 years: 10% discount
        - 65 years and above: 15% discount

        Disability Discount:
        - Disabled: 25% discount

        Pre-existing Medical Conditions Discounts:
        - Diabetes**: 10% discount
        - Hypertension: 10% discount
        - Chronic Condition: 10% discount

        Input: Provide the customer's age, disability status (if applicable), and any pre-existing medical conditions. 

        Note: If the customer qualifies for multiple discounts, return the highest discount value.

        Examples:
        1. Input: The customer is 68 yrs old. Not Disabled. With medical conditions of: diabetes
           Output: 10% (highest discount).

        2. Input: The customer is 20 yrs old. Disabled. With medical conditions of: Diabetes, Hypertension
           Output: 25% (highest discount).

        Return only the numerical value, without any additional text or explanation.
        """

    def calculate_discount_using_llm(self) -> int:
        """Query the LLM to determine the discount percentage based on customer information.

        This method sends a request to the GPT model with customer details and retrieves
        the calculated discount percentage.

        Returns:
            int: The calculated discount percentage as an integer.

        Raises:
            ValueError: If the response from the LLM is not a valid percentage.
            Exception: For general API-related issues or connectivity problems.
        """
        try:
            # Query the GPT model with the system instructions and user prompt
            calculated_discount_from_gpt = query_gpt_model(
                system_message=self._system_message_instructions(),
                user_prompt=self.prompt,
            )

            # Check if the output is a valid percentage
            if not calculated_discount_from_gpt.isdigit():
                raise ValueError(
                    "The response from the LLM is not a valid discount percentage."
                )

            return int(calculated_discount_from_gpt)

        except ValueError as ve:
            print(f"ValueError encountered: {ve}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while querying the LLM: {e}")
            raise


async def create_customer_rental_service(
    payload: CustomerRentalsSchema,
) -> List[Dict[str, Any]]:
    """Creates a customer rental entry in the database.

    Args:
        payload (CustomerRentalsSchema): The payload containing customer rental details.

    Returns:
        List[Dict[str, Any]: The created customer rental entry data.

    Raises:
        ValueError: If the customer cannot be found or if any data is invalid.
    """
    try:
        # Retrieve the customer information from the database
        customer_records = retrieve_query(
            table="customers",
            columns=[
                "id",
                "created_at",
                "name",
                "age",
                "contact_info",
                "is_disabled",
                "medical_conditions",
            ],
            filters={"id": payload.customer_id},
        )

        # Check if the customer was found
        if not customer_records:
            raise Exception("Customer not found")

        customer_info = customer_records[0]
        logging.info(f"Customer found: {customer_info.get('name')}")

        # Extract customer details
        customer_age: int = customer_info.get("age")
        customer_is_disabled: bool = customer_info.get("is_disabled")
        customer_medical_conditions: List[str] = customer_info.get(
            "medical_conditions", []
        )

        # Create a customer information message
        medical_conditions_info = (
            ", ".join(customer_medical_conditions)
            if customer_medical_conditions
            else "None"
        )
        customer_details_message: str = (
            f"The customer is {customer_age} years old. "
            f"{'Disabled' if customer_is_disabled else 'Not Disabled'}. "
            f"Medical conditions: {medical_conditions_info}."
        )
        logging.info(f"Customer info: {customer_details_message}")

        # Calculate total discount based on customer information
        discount_calculator = DiscountCalculator(prompt=customer_details_message)
        total_discount = discount_calculator.calculate_discount_using_llm()

        # Calculate the total fee after applying the discount
        total_fee: float = payload.rental_fee - total_discount

        # Prepare customer rental data for insertion
        customer_rental_data: Dict[str, Any] = {
            "customer_id": payload.customer_id,
            "rental_date": datetime.date.today().strftime("%Y-%m-%d"),
            "shoe_size": payload.shoe_size,
            "rental_fee": payload.rental_fee,
            "discount": total_discount,
            "total_fee": round(total_fee, 2),
        }

        # Insert the rental data into the database
        created_rental_record = create_query(
            table="customer_rentals", data=customer_rental_data
        )
        return created_rental_record

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while creating customer rental: {e}")
        raise
