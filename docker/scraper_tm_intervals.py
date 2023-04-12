from jinja2 import Environment, FileSystemLoader


# Путь к каталогу с шаблонами
STATIC_DIR = Environment(loader=FileSystemLoader("static/"))


# Модель метрик для prometheus
class Metric:
    def __init__(self, title: str, interval: int, desc: str = 'N/A'):
        self.title = title
        self.interval = interval
        self.desc = desc


list_metrics = [
    Metric('python', 300), Metric('math', 60)
]


# Класс
class TMScrapeMetrics:
    def __init__(self, metrics=None):
        """

        :param metrics: list of items Metric type
        """
        # metrics default
        if metrics is None:
            metrics = list_metrics

        # path to template
        self.template = STATIC_DIR.get_template("metrics.html")

        # page content
        self.content = {
            'metrics': metrics
        }

        # ready-made markup in str format
        self.metrics_markup = self.template.render(self.content)

    # dander funk repr convert str markup to bytes
    def __repr__(self):
        return str.encode(self.metrics_markup)


class TMScrapeIndex:
    def __init__(self):
        # path to template
        self.template = STATIC_DIR.get_template("index.html")

        # page content
        self.content = {
            'base_version': "5.1",
            'last_commit': "https://github.com/Samson-P/TimeManager/commit/448f1afe5515029a0ddb3cb665859524c1a7f0e9",
            'metrics_url': "/metrics"}  # tm-prom:9092/metrics

        # ready-made markup in str format
        self.metrics_markup = self.template.render(self.content)

    # dander funk repr convert str markup to bytes
    def __repr__(self):
        return str.encode(self.metrics_markup)
