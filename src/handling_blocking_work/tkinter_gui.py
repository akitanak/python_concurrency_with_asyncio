from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import ttk
from .stress_test_class import StressTest


class LoadTester(Tk):
    _load_test: StressTest = None

    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.loop = loop

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)

        self._url_field = Entry(self, width=10)
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(text="Number of requests:")
        self._request_label.grid(column=0, row=1)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)

        self._pb = ttk.Progressbar(
            self, orient="horizontal", length=200, mode="determinate"
        )
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):
        if pct == 100:
            self._load_test = None
            self._submit["text"] = "Submit"

        self._pb["value"] = pct

    def _trigger_update(self, completed_requests: int, total_requests: int):
        self.after_idle(
            self._update_bar, int((completed_requests / total_requests) * 100)
        )

    def _start(self):
        if self._load_test is None:
            self._submit["text"] = "Cancel"
            test = StressTest(
                self._loop,
                self._url_field.get(),
                int(self._request_field.get()),
                self._trigger_update,
            )
            test.start()
            self._load_test = None
            self._submit["text"] = "Submit"
