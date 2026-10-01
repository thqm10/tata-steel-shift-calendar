"""Config flow for Tata Steel ploegendienst kalender."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_TEAM,
    DOMAIN,
    TEAM_COLORS,
    roster_title,
    team_display_name,
)


def _schema(
    team_color: str = "red",
    language: str = "nl",
) -> vol.Schema:
    """Return the configuration schema."""
    options = sorted(
        TEAM_COLORS,
        key=lambda color: team_display_name(color, language).casefold(),
    )

    return vol.Schema(
        {
            vol.Required(CONF_TEAM, default=team_color): SelectSelector(
                SelectSelectorConfig(
                    options=options,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key="team_color",
                )
            )
        }
    )


class TataSteelShiftCalendarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle configuration for Tata Steel ploegendienst kalender."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Configure one Tata Steel team-color roster."""
        if user_input is not None:
            team_color = str(user_input[CONF_TEAM])
            self._async_abort_entries_match({CONF_TEAM: team_color})
            return self.async_create_entry(
                title=roster_title(team_color, self.hass.config.language),
                data={CONF_TEAM: team_color},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(language=self.hass.config.language),
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Allow changing the configured team color."""
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            team_color = str(user_input[CONF_TEAM])
            for existing in self.hass.config_entries.async_entries(DOMAIN):
                if (
                    existing.entry_id != entry.entry_id
                    and existing.data.get(CONF_TEAM) == team_color
                ):
                    return self.async_abort(reason="already_configured")

            return self.async_update_reload_and_abort(
                entry,
                data_updates={CONF_TEAM: team_color},
                title=roster_title(team_color, self.hass.config.language),
                reload_even_if_entry_is_unchanged=False,
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_schema(
                str(entry.data[CONF_TEAM]),
                self.hass.config.language,
            ),
        )
