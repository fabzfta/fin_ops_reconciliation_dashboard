"""
HubSpot CRM Pipelines API.

This module retrieves CRM pipeline metadata from HubSpot.

Pipeline metadata should be retrieved dynamically instead of
hardcoding internal HubSpot IDs in the application.

For Deals, a pipeline defines the sales process and contains stages
such as:

- Appointment Scheduled
- Qualified to Buy
- Presentation Scheduled
- Decision Maker Bought-In
- Contract Sent
- Closed Won
- Closed Lost
"""

from .clients import HubSpotClient


class HubSpotPipelines:
    """
    Service responsible for retrieving HubSpot CRM pipelines.
    """

    ENDPOINT = "/crm/v3/pipelines"

    def __init__(self, client: HubSpotClient):
        """
        Initialize the Pipelines service.

        Args:
            client:
                Authenticated HubSpotClient instance.
        """
        self.client = client

    def get_deal_pipelines(self) -> dict:
        """
        Retrieve all pipelines configured for Deal objects.

        Returns:
            dict:
                HubSpot response containing Deal pipelines
                and their stages.
        """

        endpoint = f"{self.ENDPOINT}/deals"

        return self.client.get(endpoint)


    def find_pipeline_by_label(
        self,
        pipeline_label: str,
    ) -> dict:
        """
        Find a Deal pipeline by its human-readable label.

        Args:
            pipeline_label:
                Pipeline label as configured in HubSpot.

                Example:
                "Sales Pipeline"

        Returns:
            dict:
                Pipeline metadata.

        Raises:
            ValueError:
                If the requested pipeline cannot be found.
        """

        response = self.get_deal_pipelines()

        for pipeline in response.get("results", []):
            if pipeline.get("label") == pipeline_label:
                return pipeline

        raise ValueError(
            f"Pipeline '{pipeline_label}' was not found."
        )


    def find_stage_by_label(
        self,
        pipeline: dict,
        stage_label: str,
    ) -> dict:
        """
        Find a stage inside a HubSpot pipeline.

        Args:
            pipeline:
                Pipeline metadata returned by HubSpot.

            stage_label:
                Human-readable stage label.

                Example:
                "Qualified To Buy"

        Returns:
            dict:
                Stage metadata.

        Raises:
            ValueError:
                If the stage cannot be found.
        """

        for stage in pipeline.get("stages", []):
            if stage.get("label") == stage_label:
                return stage

        raise ValueError(
            f"Stage '{stage_label}' was not found "
            f"in pipeline '{pipeline.get('label')}'."
        )


if __name__ == "__main__":
    client = HubSpotClient()

    pipelines = HubSpotPipelines(client)

    result = pipelines.get_deal_pipelines()

    print(result)