from aiogram_dialog.widgets.text import Jinja, Text
from jinja2 import Template

main_menu = "Главное меню"
welcome_text = str("Добро пожаловать\n" "Выберите интересующий вас пункт в меню")

const_text_list_service_token = (
    "Выберите блокчейн смарт-контракта\n"
)


def status_to_icon(status, follower_type=None):
    status_icons = {
        1: "✅",
        2: "🚫",
        3: "⚠️",
    }

    follower_icons = {
        "facebook_followers": "📘",
        "twitter_followers": "🐦",
        "reddit_followers": "👽",
        "telegram_followers": "📲",
        "github_stars": "⭐",
    }

    if follower_type:
        return follower_icons.get(follower_type, "None")
    else:
        return status_icons.get(status, "None")


# Prepare sc_base_info_template with globals
sc_base_info_template_string = """
{% if not has_base_analyse %} Анализ невозможен, так как {{error_msg}} {% else %}
<b>Token Information</b>
{% if name is not none %} Имя: {{ name }} {% endif %}
{% if token_symbol is not none %} Symbol: {{ token_symbol }} {% endif %}
Результат исследования смарт-контракт <b>{{token_adr}}</b> в сети <b>{{network_name}}</b>
<i>Creator:</i>
{% if creator.adr is not none %} Address: {{ creator.adr }} {% else %} Creator не обнаружен {% endif %} \
{% if creator.balance is not none %} Balance: {{ creator.balance }} {% endif %} \
{% if creator.rate is not none %} Rate: {{ creator.rate }} {{ status_to_icon(creator_balance_rate.status) }} {% endif %}
<i>Owner:</i>
{% if owner.adr is not none %} Address: {{ owner.adr }} {% else %} Owner не обнаружен {% endif %} \
{% if owner.balance is not none %} Balance: {{ owner.balance }} {% endif %} \
{% if owner.rate is not none %} Rate: {{ owner.rate }} {{ status_to_icon(owner_balance_rate.status) }} {% endif %} 
<i>Other Properties</i>
Has verified source code: {{status_to_icon(has_source_code)}}
Is Renounced: {{ status_to_icon(is_renounced.status) }}
Is Proxy: {{ status_to_icon(is_proxy.status) }}
Is Mintable: {{ status_to_icon(is_mintable.status) }}
Is Burnable: {{ status_to_icon(is_burnable.status) }}
Is Self Destructable: {{ status_to_icon(is_self_destructable.status) }}
Is Token Transferable: {{ status_to_icon(is_token_transferable.status) }}
{% endif %}"""
sc_base_info_template = Template(sc_base_info_template_string)
sc_base_info_template.globals['status_to_icon'] = status_to_icon


# Window Definition
class CustomJinjaForBaseInfo(Text):
    async def _render_text(self, data, dialog_manager):
        return sc_base_info_template.render(data)


# Prepare Jinja sc_source_code_analytic_template
sc_source_code_analytic_template_string = """
{% if not source_code_not_analyzed %}
{% if has_error %}
<b>Errors Found:</b>
{% for error in enriched_erros_data_output %}
  <b>Name:</b> {{ error.name }}
  <b>Cases:</b> {{ error.cases }}
  <b>Severity:</b> {% if error.severity == "Informational" %}🔵 {{ error.severity }}
  {% elif error.severity == "Optimization" %}🟢 {{ error.severity }}
  {% elif error.severity == "Low" %}🟡 {{ error.severity }}
  {% elif error.severity == "Medium" %}🟠 {{ error.severity }}
  {% elif error.severity == "High" %}🔴 {{ error.severity }}
  {% else %}{{ error.severity }}
  {% endif %}
  <b>Confidence:</b> {{ error.confidence }}
{% endfor %}
{% else %}
<b>No Errors Found.</b>
{% endif %}
{% endif %}
"""
sc_source_code_analytic_template = Template(sc_source_code_analytic_template_string)


# Custom Text widget for Jinja rendering
class CustomSourceCodeAnalyticJinja(Text):
    async def _render_text(self, data, dialog_manager):
        return sc_source_code_analytic_template.render(data)


# Jinja template to display liquidity data
sc_liquidity_template_string = """
{% if pancakeswapv2 %} \
<b>PancakeSwap V2 Pools:</b> \
{% for pool in pancakeswapv2 %}
  <b>Type:</b> {{ pool.type }}
  <b>Pool Address:</b> {{ pool.pool_adr }}
  <b>Base Coin:</b> {{ pool.base_coin }}
  <b>Pool Fee (%):</b> {{ pool.pool_fee }}
  <b>Amount:</b> {{ pool.amount }}
  <b>Price:</b> {{ pool.price }}
{% endfor %} {% endif %} \
{% if pancakeswapv3 %} \
<b>PancakeSwap V3 Pools:</b> \
{% for pool in pancakeswapv3 %}
  <b>Type:</b> {{ pool.type }}
  <b>Pool Address:</b> {{ pool.pool_adr }}
  <b>Base Coin:</b> {{ pool.base_coin }}
  <b>Pool Fee (%):</b> {{ pool.pool_fee }}
  <b>Amount:</b> {{ pool.amount }}
  <b>Price:</b> {{ pool.price }}
{% endfor %} {% endif %} \
{% if uniswapv2 and uniswapv2 | length > 0%} \
<b>Uniswap V2 Pools:</b> \
{% for pool in uniswapv2 %}
  <b>Type:</b> {{ pool.type }}
  <b>Pool Address:</b> {{ pool.pool_adr }}
  <b>Base Coin:</b> {{ pool.base_coin }}
  <b>Pool Fee (%):</b> {{ pool.pool_fee }}
  <b>Amount:</b> {{ pool.amount }}
  <b>Price:</b> {{ pool.price }}
{% endfor %} {% endif %} \
{% if uniswapv3 and uniswapv3 | length > 0 %} \
<b>Uniswap V3 Pools:</b> \
{% for pool in uniswapv3 %}
  <b>Type:</b> {{ pool.type }}
  <b>Pool Address:</b> {{ pool.pool_adr }}
  <b>Base Coin:</b> {{ pool.base_coin }}
  <b>Pool Fee (%):</b> {{ pool.pool_fee }}
  <b>Amount:</b> {{ pool.amount }}
  <b>Price:</b> {{ pool.price }}
{% endfor %} {% endif %}
"""
sc_liquidity_template = Template(sc_liquidity_template_string)
sc_empty_sc_liquidity_template = Template("""<b>No Liquidity Found.</b>""")


# Custom Text widget for Jinja rendering
class CustomLiquidityJinja(Text):
    async def _render_text(self, data, dialog_manager):
        text_html = sc_liquidity_template.render(data)
        if text_html is None or len(text_html.strip()) < 1:
            return sc_empty_sc_liquidity_template.render(data)
        return sc_liquidity_template.render(data)


sc_transfer_info_template_string = """
{% if transfer_info %}
<b>Transfer Information</b>
Глубокий анализ передачи монет смарт-контракта
<i>Переданное количество:</i>
Value: {{ transfer_info.transfer_delivered.value }} Status: {{ status_to_icon(transfer_info.transfer_delivered.status) }}
<i>Взимаемый процент:</i>
Value: {{ transfer_info.transfer_percent.value }} Status: {{ status_to_icon(transfer_info.transfer_percent.status) }}
{% else %} Точная передача токенов не получена {% endif %}"""
sc_transfer_info_template = Template(sc_transfer_info_template_string)
sc_transfer_info_template.globals['status_to_icon'] = status_to_icon


class CustomJinjaForTransferInfo(Text):
    async def _render_text(self, data, dialog_manager):
        return sc_transfer_info_template.render(data)


social_info_template_string = """
{% if social_info %}
{% if social_info.interest_rate != -1 %} <b>Интересуются (%):</b> {{ social_info.interest_rate }} \n {% endif %} \
{% if social_info.ignore_rate != -1 %} <b>Игнорируют (%):</b>{{ social_info.ignore_rate }} \n {% endif %} \
{% if social_info.attractiveness_score != -1 %}<b>Общая оценка привлекательности токена (%):</b> {{ social_info.attractiveness_score }} \n {% endif %} \
{% if social_info.engagement_score != -1 %}<b>Оценка вовлеченности в разработку (%):</b> {{ social_info.engagement_score }} \n {% endif %} \
{% if social_info.liquidity_score != -1 %}<b>Оценка ликвидности:</b> {{ social_info.liquidity_score }} \n {% endif %} \
{% if social_info.community_score != -1 %}<b>Оценка community токена:</b> {{ social_info.community_score }} \n {% endif %}
<b>Рыночный рейтинг привлекательности:</b> {{ social_info.market_ranking }}
{% if social_info.coingecko_rank != -1 %}<b>Рейтинг coingecko:</b> {{ social_info.coingecko_rank }} \n {% endif %} \
{% if social_info.facebook_followers is not none %} {{ status_to_icon(None, "facebook_followers") }} <b>Подписчики Facebook:</b> {{ social_info.facebook_followers }} \n {% endif %} \
{% if social_info.twitter_followers is not none %} {{ status_to_icon(None, "twitter_followers") }} <b>Подписчики Twitter:</b> {{ social_info.twitter_followers }} \n {% endif %} \
{% if social_info.reddit_followers is not none %} {{ status_to_icon(None, "reddit_followers") }} <b>Подписчики Reddit:</b> {{ social_info.reddit_followers }} \n {% endif %} \
{% if social_info.telegram_followers is not none %} {{ status_to_icon(None, "telegram_followers") }} <b>Подписчики Telegram:</b> {{ social_info.telegram_followers }} \n {% endif %} \
{% if social_info.github_stars is not none %} {{ status_to_icon(None, "github_stars") }} <b>GitHub Stars:</b> {{ social_info.github_stars }} \n {% endif %} \
{% if social_info.github_followers is not none %}<b>Подписчики GitHub:</b> {{ social_info.github_followers }}{% endif %}
{% else %} Социальная активность не обнаружена. {{ error_msg }} {% endif %}
"""

social_info_template = Template(social_info_template_string)
social_info_template.globals['status_to_icon'] = status_to_icon


class CustomJinjaForSocialInfo(Text):
    async def _render_text(self, data, dialog_manager):
        return social_info_template.render(data)

    async def render(self, data):
        return self._render_text(data, None)


sc_ai_analyze_template_string = """
{% if ai_analyze_result %}
<b>Мошеннеческий контракт:</b> {{ ai_analyze_result.is_fraud }}
<b>Мера предсказания:</b> {{ ai_analyze_result.ai_data }}
{% else %} Ai-анализ не выполнен {{ error_msg }} {% endif %}
"""

ai_analyze_template = Template(sc_ai_analyze_template_string)
# ai_analyze_template.globals['status_to_icon'] = status_to_icon


class CustomJinjaForAiAnalyze(Text):
    async def _render_text(self, data, dialog_manager):
        return ai_analyze_template.render(data)


sc_combined_template_string = sc_base_info_template_string + social_info_template_string + \
                              sc_ai_analyze_template_string + sc_source_code_analytic_template_string + \
                              sc_liquidity_template_string + sc_transfer_info_template_string
sc_combined_template = Template(sc_combined_template_string)
sc_combined_template.globals['status_to_icon'] = status_to_icon


# Custom Text widget for Jinja rendering
class CustomFullInfoJinja(Text):
    async def _render_text(self, data, dialog_manager):
        return sc_combined_template.render(data)


wrap_deeper_info_about_sc = Jinja(
    text="""
Вы глубже выбрали токен <b>{{token_name}}</b>
"""
)


text_command_start = (
    "Добро пожаловать!\n" "Чтобы воспользоваться нашим сервисом введите команду /menu"
)


def text_about_choosen_provider(provider: str) -> str:
    text = (
        f"Оставляем выбранного провайдера {provider}"
    )
    return text


if __name__ == "__main__":
    for i, v in enumerate(["test", "pol"]):
        print(i, v)
    print("main")
