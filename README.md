# 🎂 40th Birthday Trip Assistant - Ultimate Edition

**Complete Production-Quality Trip Planner**

Your comprehensive Amelia Island adventure companion - a beautiful, feature-rich Streamlit application for planning, managing, and experiencing your 40th birthday celebration trip.

---

## ✨ Features

### 🏠 **Interactive Dashboard**
- Real-time trip countdown with days/hours remaining
- Comprehensive trip metrics and progress tracking
- Action items with priority indicators
- Booking status overview
- Weather snapshot with alerts
- Visual progress bars for meal/activity planning

### 📅 **Smart Schedule Management**
- **Full Schedule**: Complete day-by-day timeline
- **Today View**: Context-aware daily briefing
- **Conflict Detection**: Automatic overlap detection with visual timeline
- **Calendar Export**: iCal format for Google/Apple Calendar
- Travel time calculations between locations
- Status tracking (Confirmed, Urgent, Pending, Optional)

### 🍽️ **Collaborative Meal Planning**
- 8 meal slots (Saturday breakfast through Tuesday breakfast)
- 3+ restaurant options per meal
- Voting system for you and John
- Restaurant details: cuisine, cost, phone, booking links
- Non-seafood options clearly marked
- Final selection confirmation and reservation tracking

### 🎯 **Activity Proposals**
- 7 activity time slots
- Multiple options per slot with voting
- Detailed activity information (cost, duration, location)
- Booking integration with confirmation tracking
- Custom activity creation

### 📞 **Booking Dashboard**
- Urgency-based prioritization (critical/high/normal)
- Days-until countdown for each booking
- One-click phone dialing
- Confirmation number tracking
- Quick actions (copy all numbers, email list)
- Booking status management

### 🌤️ **Weather Intelligence**
- 6-day forecast with detailed conditions
- UV index monitoring with protection recommendations
- Hourly tide schedule for beach activities
- **Smart Weather Alerts**:
  - Rain warnings for outdoor activities
  - UV alerts for extended sun exposure
  - Wind warnings for boat tours
  - Heat advisories with hydration reminders
- Daily weather briefings

### 🗺️ **Interactive Maps**
- All locations plotted on interactive map
- Distance calculations from hotel
- Drive time estimates
- Visual route planning
- Location details with addresses and phones

### 🎒 **Smart Packing List**
- Auto-generated based on confirmed activities
- Weather-adaptive suggestions
- Category organization (Clothing, Toiletries, Electronics, etc.)
- Checkbox progress tracking
- Saves packing progress

### 💰 **Budget Tracking**
- Category-wise expense tracking
- Confirmed vs. pending costs
- Visual budget charts
- Running total and spending analysis
- Trip-wide budget overview

### 🚗 **Travel Intelligence**
- Real-time flight status tracking
- Airport information
- TSA wait times
- Gate updates
- Travel time calculations

### 💆 **Spa Treatment Guide**
- Complete Ritz-Carlton spa menu
- Treatment descriptions and pricing
- Duration estimates
- Direct booking information
- Couples treatments highlighted

### 📸 **Memories & Journal**
- Photo upload and gallery
- Journal entries by date
- Highlight special moments
- Trip recap with statistics
- Exportable memories

### 🔔 **Smart Notifications**
- Booking reminders
- Weather alerts
- Activity reminders
- Custom notifications

### 🔒 **Security & Privacy**
- Password protection (contact repository owner for password)
- Public view mode (hides sensitive data)
- Atomic file operations (no data corruption)
- Automatic backups (last 20 saves)
- Change audit trail

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd 40thBdayAppRebuild
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp env.example .env
   # Edit .env with your actual API keys
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`
   - **Password**: Contact repository owner for password

---

## 📱 Using the App

### For Michael (Trip Planner)

#### **Before the Trip:**

1. **Complete Meal Planning**
   - Go to "Meal Proposals" page
   - Review 8 meal options
   - Vote on your preferences
   - Wait for John to vote
   - Finalize choices and make reservations

2. **Finalize Activities**
   - Go to "Activity Proposals" page
   - Review 7 activity slots
   - Vote on preferences
   - Coordinate with John
   - Book confirmed activities

3. **Make All Bookings**
   - Go to "Bookings" dashboard
   - Call each business to book (one-click dial)
   - Mark as booked with confirmation numbers
   - Track status until all confirmed

4. **Check Schedule**
   - Go to "Full Schedule" page
   - Review complete timeline
   - Run conflict detector (automatic)
   - Fix any overlaps or tight transitions
   - Export calendar to your phone

5. **Pack**
   - Go to "Packing List" page
   - Review auto-generated list
   - Check off items as you pack
   - Add any personal items

6. **Final Check**
   - Dashboard shows overall readiness percentage
   - Address any red/yellow action items
   - Export everything you need offline
   - Share schedule with John

#### **During the Trip:**

1. **Each Morning**
   - Check "Today" page for daily briefing
   - Review weather and any alerts
   - Confirm first activity of the day

2. **Capture Memories**
   - Upload photos to Memories page
   - Write journal entries
   - Mark special highlights

3. **Track Budget**
   - Update actual spending in Budget page
   - Compare to estimates

### For John (Participant)

1. **Review Schedule**
   - Go to "John's Page" for your personalized view
   - See when you arrive/depart
   - Review all activities you'll participate in

2. **Vote on Choices**
   - Meal Proposals: Vote on restaurant preferences
   - Activity Proposals: Vote on activity preferences
   - Michael will finalize based on votes

3. **Stay Informed**
   - Check schedule before trip
   - Know meeting points and times
   - Have hotel and Michael's contact info

---

## 🎯 Trip Details

**Dates**: November 7-11, 2025
**Location**: The Ritz-Carlton, Amelia Island
**Hotel Phone**: (904) 277-1100
**Travelers**: Michael (arrives Friday) + John (arrives Saturday, leaves Tuesday)

### Key Contacts
- **Hotel**: (904) 277-1100
- **Spa**: (904) 277-1087
- **Boat Tour**: (904) 753-7631

---

## 🔧 Configuration

### Changing the Password

**Generate new password hash:**
```bash
echo -n "your_new_password" | md5 | tr -d '\n'
```

**Update in code:**
```python
# In app.py, find this line and update the hash:
if hashlib.md5(password_input.encode()).hexdigest() == 'YOUR_NEW_HASH_HERE':
```

**Or use environment variable:**
```bash
export TRIP_PASSWORD_HASH='your_new_hash'
```

### Weather API Setup (Optional)

The app uses OpenWeather API for real-time weather:

1. Get free API key at [OpenWeather](https://openweathermap.org/api)
2. Add to environment:
   ```bash
   export OPENWEATHER_API_KEY='your_api_key'
   ```
3. Restart the app

Without API key, app uses fallback weather data.

### GitHub Storage

The app uses GitHub for data persistence:

1. Create personal access token at GitHub Settings > Developer Settings
2. Set environment variables:
   ```bash
   export GITHUB_TOKEN='your_token'
   export GITHUB_REPO='username/repo'
   ```

### Custom Data

**Add your own activities:**
Edit `get_activities_and_timeline()` function in `app.py`

**Add meal options:**
Use the "Meal Proposals" page in the app (no code changes needed!)

**Add activity options:**
Use the "Activity Proposals" page in the app

---

## 🚢 Deployment

### Streamlit Community Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy on Streamlit**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repository
   - Select `app.py`
   - Add secrets (API keys, passwords)
   - Deploy!

3. **Configure Secrets**
   ```toml
   # .streamlit/secrets.toml (or in Streamlit dashboard)
   OPENWEATHER_API_KEY = "your_key"
   TRIP_PASSWORD_HASH = "your_hash"
   GITHUB_TOKEN = "your_token"
   ```

### Other Platforms

**Heroku:**
```bash
heroku create your-app-name
git push heroku main
```

**Railway:**
```bash
railway login
railway init
railway up
```

**Render:**
- Connect GitHub repo in Render dashboard
- Set environment variables
- Deploy automatically

---

## 🧪 Testing

### Run Test Suite
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_schedule_checker.py -v
```

### Test Coverage
- Data management (atomic writes, backups)
- Schedule conflict detection
- Data validation
- Export functionality (iCal, text)
- Weather alerts
- Packing list generation

See `tests/README.md` for detailed testing guide.

### Data Validation
```bash
# Run validation on trip data
python validate_data_simple.py
```

---

## 📊 Project Structure

```
40thBdayAppRebuild/
├── app.py                          # Main Streamlit application (10K+ lines)
├── github_storage.py               # GitHub data persistence
├── data_operations.py              # CRUD operations for proposals
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── TRIP_GUIDE.md                  # User guide for the trip
├── TRIP_PREPARATION_CHECKLIST.md  # Pre-trip checklist
│
├── data/
│   ├── trip_data.json             # Main data file (meals, activities, bookings)
│   └── backups/                   # Automatic backups (last 20)
│
├── pages/
│   └── bookings.py                # Booking dashboard page
│
├── utils/
│   ├── data_manager.py            # TripDataManager (atomic writes, backups)
│   ├── data_validator.py          # Data validation and integrity checks
│   ├── schedule_checker.py        # Conflict detection and timeline viz
│   ├── weather_alerts.py          # Smart weather alert generation
│   └── exports.py                 # Calendar (iCal) and text exports
│
├── tests/
│   ├── test_data_manager.py       # Tests for data persistence
│   ├── test_schedule_checker.py   # Tests for conflict detection
│   ├── test_data_validator.py     # Tests for data validation
│   ├── test_exports.py            # Tests for export functionality
│   ├── test_weather_alerts.py     # Tests for weather alerts
│   └── README.md                  # Testing documentation
│
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

---

## 🎨 Design Features

### Visual Design
- **Modern UI**: Clean, professional design with smooth animations
- **Color Coding**: Status-based colors (red=urgent, yellow=warning, green=confirmed)
- **Responsive**: Works beautifully on desktop, tablet, and mobile
- **Dark Mode**: Not yet implemented (future enhancement)

### UX Features
- **Progressive Disclosure**: Information revealed as needed
- **Contextual Help**: Tooltips and explanations throughout
- **Keyboard Shortcuts**: Standard Streamlit shortcuts work
- **Accessible**: High contrast, clear typography

### Performance
- **Caching**: Smart caching for weather and data
- **Lazy Loading**: Heavy features load on-demand
- **Optimized Images**: Efficient image handling
- **Fast Rendering**: Sub-second page loads

---

## 📈 Feature Roadmap

### Current Status: **Production Ready** ✅

### Completed Features ✅
- [x] Dashboard with metrics
- [x] Full schedule management
- [x] Booking tracker with CRUD
- [x] Schedule conflict detection
- [x] Weather alerts
- [x] Calendar export (iCal)
- [x] Packing list generator
- [x] Budget tracking
- [x] Interactive maps
- [x] Meal voting system
- [x] Activity voting system
- [x] Data validation
- [x] Atomic file operations
- [x] Automatic backups
- [x] Test suite
- [x] Comprehensive documentation

### Potential Future Enhancements 💡
- [ ] PDF schedule export
- [ ] Email notifications
- [ ] SMS reminders
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Trip templates
- [ ] Expense receipt uploads
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] Offline PWA mode

---

## 🆘 Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for conflicting packages
pip check
```

**Password not working:**
- Contact repository owner for password
- If changed, verify MD5 hash matches
- Clear browser cache/cookies

**Data not saving:**
- Check `data/` directory exists
- Verify write permissions
- Check `data/backups/` directory exists
- Review `data/change_log.txt` for errors

**GitHub storage issues:**
- Verify `GITHUB_TOKEN` is valid
- Check repository permissions
- Confirm `trip_data.json` exists in repo

**Weather not loading:**
- Check internet connection
- Verify `OPENWEATHER_API_KEY` is set
- Free API tier has rate limits (60 calls/min)
- App will use fallback data if API fails

**Schedule conflicts not detected:**
- Verify all activities have valid dates/times
- Check date format is YYYY-MM-DD
- Check time format is HH:MM AM/PM
- Run conflict detector manually on Full Schedule page

**Tests failing:**
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run with verbose output
pytest tests/ -v -s

# Check specific test
pytest tests/test_schedule_checker.py::TestScheduleConflicts::test_overlap_detected -v
```

### Getting Help

1. **Check Documentation**
   - This README
   - `TRIP_GUIDE.md` for usage
   - `tests/README.md` for testing
   - `TRIP_PREPARATION_CHECKLIST.md` for trip planning

2. **Check Logs**
   - Browser console (F12) for frontend errors
   - Terminal output for backend errors
   - `data/change_log.txt` for data operations

3. **Validate Data**
   ```bash
   python validate_data_simple.py
   ```

4. **Reset to Clean State**
   ```bash
   # Backup current data
   cp data/trip_data.json data/trip_data_backup.json

   # Restore from backup
   cp data/backups/trip_data_YYYYMMDD_HHMMSS.json data/trip_data.json
   ```

---

## 🔐 Security

### Data Protection
- **Atomic Writes**: No partial/corrupted saves
- **Automatic Backups**: Last 20 versions saved
- **Change Audit Trail**: All modifications logged
- **Recovery System**: Restore from backups if needed

### Privacy
- **Password Protection**: Sensitive data hidden without password
- **Public View Mode**: Shareable without exposing personal details
- **Environment Variables**: API keys never in code
- **No Analytics**: No tracking or data collection

### Best Practices
- Don't commit `.env` file
- Keep API keys secret
- Use strong passwords
- Rotate tokens regularly
- Review change logs periodically

---

## 📝 Documentation

### For Users
- **TRIP_GUIDE.md**: Complete guide to using the app for your trip
- **TRIP_PREPARATION_CHECKLIST.md**: Step-by-step pre-trip checklist
- **This README**: Setup, deployment, and technical details

### For Developers
- **Code Comments**: Extensive inline documentation
- **Type Hints**: Function signatures documented
- **Docstrings**: Module and function descriptions
- **tests/**: Comprehensive test coverage with examples

---

## 🤝 Contributing

This is a personal project, but if you want to adapt it:

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

This project is for personal use. Feel free to adapt it for your own trips!

---

## 🎉 Acknowledgments

**Built With:**
- [Streamlit](https://streamlit.io) - Web framework
- [Plotly](https://plotly.com) - Interactive charts
- [Folium](https://python-visualization.github.io/folium/) - Interactive maps
- [OpenWeather API](https://openweathermap.org/api) - Weather data
- [Pandas](https://pandas.pydata.org/) - Data manipulation

**Special Thanks:**
- Claude Code for development assistance
- The Streamlit community
- GitHub for hosting and storage

---

## 🎂 Enjoy Your Trip!

Have an absolutely amazing 40th birthday celebration at Amelia Island! This app will help you stay organized and make the most of every moment.

**Trip Countdown:** November 7-11, 2025 🎉

---

*Made with ❤️ for an unforgettable 40th birthday celebration*

**Version**: 2.0 Ultimate Edition
**Last Updated**: October 28, 2025
**Status**: Production Ready ✅
