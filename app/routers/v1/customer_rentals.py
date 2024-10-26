import logging
from typing import List, Union

from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from app.queries import retrieve_query
from app.schema import CustomerRentalsResponseSchema, CustomerRentalsSchema
from app.services.customer_rentals_services import create_customer_rental_service

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(tags=["Customer Rentals v1"])


@router.post("/customer/rentals/", response_model=List[CustomerRentalsResponseSchema])
async def create_customer_rental(
    payload: CustomerRentalsSchema,
) -> Union[JSONResponse, HTTPException]:
    """**Create a new customer rental entry in the database.**

    **Args**:
    - **payload (CustomerRentalsSchema)**: Data for the customer rental to be created.
        - **customer_id (int)**: ID of the customer.
        - **shoe_size (int)**: Size of the shoe.
        - **rental_fee (float)**: Fee of the rental.

    **Returns**:
    - **JSONResponse**: JSON response with created customer rental entry.

    **Raises**:
    - **HTTPException**: If an error occurs during the creation process.
    """
    try:
        logger.info("Request received to create a new customer rental.")

        # Call the service to create the customer rental entry
        created_rental = await create_customer_rental_service(payload=payload)

        logger.info(
            f"Successfully created customer rental with ID: {created_rental[0]['id']}"
        )

        # Return JSON response with status 201 and created rental data
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_rental)

    except Exception as e:
        logger.error(f"Error while creating customer rental: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while creating the customer: {str(e)}",
        )


@router.get("/customer/rentals/", response_model=List[CustomerRentalsResponseSchema])
async def get_customer_rentals() -> Union[JSONResponse, HTTPException]:
    """**Retrieve a list of customer rentals from the database.**

    **Returns**:
    - **JSONResponse**: JSON response containing the list of customer rentals.

    **Raises**:
    - **HTTPException**: If an error occurs during the retrieval process.
    """
    try:
        logger.info("Request received to retrieve the list of customer rentals.")

        # Fetch customer rental data from the database
        customer_rentals = retrieve_query(
            table="customer_rentals",
            columns=[
                "id",
                "created_at",
                "customer_id",
                "rental_date",
                "shoe_size",
                "rental_fee",
                "discount",
                "total_fee",
            ],
        )

        logger.info(
            f"Successfully retrieved {len(customer_rentals)} customer rental records."
        )

        # Return JSON response with retrieved customer rental records
        return JSONResponse(status_code=status.HTTP_200_OK, content=customer_rentals)

    except Exception as e:
        logger.error(f"Error while retrieving customer rental list: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while retrieving the customer: {str(e)}",
        )
