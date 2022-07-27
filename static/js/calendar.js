// Render a calendar
function draw_calendar(data){
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    initialDate: data.start,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: data,
    eventColor: '#79cae5'
  });

  calendar.render();
}

fetch('/update_calendar')
.then((response) => response.json())
.then((data) => {
const calendar_data = data;
draw_calendar(calendar_data);
})