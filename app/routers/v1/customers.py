import logging
from typing import List, Union

from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from app.queries import create_query, retrieve_query
from app.schema import CustomerResponseSchema, CustomerSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(tags=["Customers v1"])


@router.post("/customers", response_model=List[CustomerResponseSchema])
async def create_customer(
    payload: CustomerSchema,
) -> Union[JSONResponse, HTTPException]:
    """**Create a new customer entry.**

    This endpoint registers a new customer in the `customers` table in supabase with the provided data.

    **Request Body**:
    - **payload** (*CustomerSchema*): JSON object containing the customer's details such as name, email, and phone.
        - **name (str)**: Name of the customer
        - **age (int)**: Age of the customer
        - **contact_info (List[CustomerContactInfoSchema])**: List of contact information for the customer.
            - **contact_number (str)**: Contact number for the customer.
            - **email_address (str)**: Email address of the customer.
            - **address (str)**: Address of the customer.
        - **is_disabled (bool)**: Whether the customer is disabled.
        - **medical_conditions (Optional[List[str]])**: List of medical conditions for the customer.
    **Returns**:
    - **201 Created**: Returns a JSON object with the created customer's data upon successful creation.
    - **500 Internal Server Error**: An error response if customer creation fails.

    **Raises**:
    - **HTTPException (500)**: If an unexpected error occurs during the creation process.
    """
    try:
        logger.info(f"Attempting to create a customer with data: {payload}")

        # Create the customer entry in the specified table
        customer = create_query(table="customers", data=payload.model_dump())

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Customer creation failed.",
            )

        logger.info(f"Customer created successfully: {customer}")
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=customer)
    except Exception as e:
        logger.error(f"Error while creating customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while creating the customer: {str(e)}",
        )


@router.get("/customers", response_model=List[CustomerResponseSchema])
async def get_customers_list() -> Union[JSONResponse, HTTPException]:
    """**Retrieve a List of Customers**

    This endpoint retrieves a list of customers from the `customers` table.

    **Returns**:
    - List[Dict[str, Any]]: A list of customer records, each represented as a dictionary.

    **Raises**:
    - HTTPException (500): If an unexpected error occurs while retrieving the customer list.
    """
    try:
        logger.info("Request received to retrieve the customers list.")

        # Call the retrieve_query function to fetch customer data
        customers = retrieve_query(
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
        )

        logger.info(f"Successfully retrieved {len(customers)} customer records.")

        # Return the retrieved customer records
        return JSONResponse(status_code=status.HTTP_200_OK, content=customers)

    except Exception as e:
        # Log the error with a clear message
        logger.error(f"Error while retrieving customer list: {e}")
        # Raise an HTTP exception with a 500 status code and error details
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while retrieving customer list: {str(e)}",
        )
