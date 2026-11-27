import type { Alert } from './model';
export interface LogEvent { id:string; time:string; source:string; ip:string; action:string; result:string; severity:'normal'|'critical'|'high'|'medium'|'low'; raw:string }
export const demoAlerts: (Alert & {source:string})[] = [
  {
    "id": "ALT-0248",
    "type": "SQL Injection",
    "ip": "192.0.2.40",
    "severity": "critical",
    "count": 3,
    "status": "new",
    "time": "14:52:10",
    "source": "Nginx"
  },
  {
    "id": "ALT-0247",
    "type": "SSH Brute Force",
    "ip": "203.0.113.7",
    "severity": "high",
    "count": 15,
    "status": "new",
    "time": "14:48:02",
    "source": "SSH"
  },
  {
    "id": "ALT-0246",
    "type": "SQL Injection",
    "ip": "192.0.2.41",
    "severity": "critical",
    "count": 2,
    "status": "ack",
    "time": "14:42:19",
    "source": "Nginx"
  },
  {
    "id": "ALT-0245",
    "type": "Web Scan",
    "ip": "198.51.100.18",
    "severity": "medium",
    "count": 8,
    "status": "new",
    "time": "14:30:08",
    "source": "Nginx"
  },
  {
    "id": "ALT-0244",
    "type": "SSH Brute Force",
    "ip": "203.0.113.10",
    "severity": "high",
    "count": 11,
    "status": "ack",
    "time": "14:18:42",
    "source": "SSH"
  },
  {
    "id": "ALT-0243",
    "type": "SSH Brute Force",
    "ip": "203.0.113.12",
    "severity": "high",
    "count": 9,
    "status": "new",
    "time": "13:57:03",
    "source": "SSH"
  }
];
export const demoEvents: LogEvent[] = [
  {
    "id": "EVT-0124",
    "time": "14:52:10",
    "source": "Nginx",
    "ip": "192.0.2.40",
    "action": "Подозрительный HTTP-запрос",
    "result": "403",
    "severity": "critical",
    "raw": "GET /search?q=[demo] HTTP/1.1 · 403"
  },
  {
    "id": "EVT-0123",
    "time": "14:48:02",
    "source": "SSH",
    "ip": "203.0.113.7",
    "action": "Неудачная авторизация",
    "result": "Отказ",
    "severity": "high",
    "raw": "sshd: Failed password for demo from 203.0.113.7"
  },
  {
    "id": "EVT-0122",
    "time": "14:46:32",
    "source": "Nginx",
    "ip": "198.51.100.4",
    "action": "GET /index.html",
    "result": "200",
    "severity": "normal",
    "raw": "GET /index.html HTTP/1.1 · 200"
  },
  {
    "id": "EVT-0121",
    "time": "14:42:19",
    "source": "Nginx",
    "ip": "192.0.2.41",
    "action": "Подозрительный HTTP-запрос",
    "result": "403",
    "severity": "critical",
    "raw": "GET /search?q=[demo] HTTP/1.1 · 403"
  },
  {
    "id": "EVT-0120",
    "time": "14:37:15",
    "source": "SSH",
    "ip": "203.0.113.21",
    "action": "Успешная авторизация",
    "result": "Успех",
    "severity": "normal",
    "raw": "sshd: Accepted publickey for demo"
  },
  {
    "id": "EVT-0119",
    "time": "14:30:08",
    "source": "Nginx",
    "ip": "198.51.100.18",
    "action": "Запрос несуществующего пути",
    "result": "404",
    "severity": "medium",
    "raw": "GET /demo-path HTTP/1.1 · 404"
  },
  {
    "id": "EVT-0118",
    "time": "14:28:05",
    "source": "Nginx",
    "ip": "198.51.100.4",
    "action": "GET /assets/main.css",
    "result": "200",
    "severity": "normal",
    "raw": "GET /assets/main.css HTTP/1.1 · 200"
  },
  {
    "id": "EVT-0117",
    "time": "14:18:42",
    "source": "SSH",
    "ip": "203.0.113.10",
    "action": "Неудачная авторизация",
    "result": "Отказ",
    "severity": "high",
    "raw": "sshd: Failed password for demo from 203.0.113.10"
  },
  {
    "id": "EVT-0116",
    "time": "14:10:12",
    "source": "Nginx",
    "ip": "192.0.2.12",
    "action": "GET /health",
    "result": "200",
    "severity": "normal",
    "raw": "GET /health HTTP/1.1 · 200"
  },
  {
    "id": "EVT-0115",
    "time": "13:57:03",
    "source": "SSH",
    "ip": "203.0.113.12",
    "action": "Неудачная авторизация",
    "result": "Отказ",
    "severity": "high",
    "raw": "sshd: Failed password for demo from 203.0.113.12"
  }
];
