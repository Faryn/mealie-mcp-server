import json
import logging
import traceback
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

from mealie import MealieFetcher
from models.mealplan import MealPlanEntry
from utils import format_error_response

logger = logging.getLogger("mealie-mcp")


def register_mealplan_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all mealplan-related tools with the MCP server."""

    @mcp.tool()
    def get_all_mealplans(
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> str:
        """Get all meal plans for the current household with pagination.

        Args:
            start_date: Start date for filtering meal plans (ISO format YYYY-MM-DD)
            end_date: End date for filtering meal plans (ISO format YYYY-MM-DD)
            page: Page number to retrieve
            per_page: Number of items per page

        Returns:
            str: JSON string containing mealplan items and pagination information
        """
        try:
            logger.info(
                {
                    "message": "Fetching mealplans",
                    "start_date": start_date,
                    "end_date": end_date,
                    "page": page,
                    "per_page": per_page,
                }
            )
            result = mealie.get_mealplans(
                start_date=start_date,
                end_date=end_date,
                page=page,
                per_page=per_page,
            )
            return json.dumps(result)
        except Exception as e:
            error_msg = f"Error fetching mealplans: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            return format_error_response(error_msg)

    @mcp.tool()
    def create_mealplan(
        entry: MealPlanEntry,
    ) -> str:
        """Create a new meal plan entry.

        Args:
            entry: MealPlanEntry object containing date, recipe_id, title, and entry_type

        Returns:
            str: JSON string containing the created mealplan entry
        """
        try:
            logger.info(
                {
                    "message": "Creating mealplan entry",
                    "entry": entry.model_dump(),
                }
            )
            result = mealie.create_mealplan(**entry.model_dump())
            return json.dumps(result)
        except Exception as e:
            error_msg = f"Error creating mealplan entry: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            return format_error_response(error_msg)

    @mcp.tool()
    def create_mealplan_bulk(
        entries: List[MealPlanEntry],
    ) -> str:
        """Create multiple meal plan entries in bulk.

        Args:
            entries: List of MealPlanEntry objects
                containing date, recipe_id, title, and entry_type
        Returns:
            str: JSON string containing the created mealplan entries
        """
        try:
            logger.info(
                {
                    "message": "Creating bulk mealplan entries",
                    "entries_count": len(entries),
                }
            )
            for entry in entries:
                mealie.create_mealplan(**entry.model_dump())
            return json.dumps({"message": "Bulk mealplan entries created successfully"})
        except Exception as e:
            error_msg = f"Error creating bulk mealplan entries: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            return format_error_response(error_msg)

    @mcp.tool()
    def get_todays_mealplan() -> str:
        """Get the mealplan entries for today.

        Returns:
            str: JSON string containing today's mealplan entries
        """
        try:
            logger.info({"message": "Fetching today's mealplan"})
            result = mealie.get_todays_mealplan()
            return json.dumps(result)
        except Exception as e:
            error_msg = f"Error fetching today's mealplan: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            return format_error_response(error_msg)
