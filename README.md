# 🎂 40th Birthday Trip Assistant

Your complete Amelia Island adventure companion - a beautiful, interactive Streamlit application for planning and managing your 40th birthday celebration trip.

## ✨ Features

### 🏠 **Interactive Dashboard**
- Real-time trip countdown and key metrics
- 6-day weather forecast with UV index
- Urgent booking alerts and status tracking
- Beautiful, responsive design optimized for mobile

### 📅 **Smart Schedule Management**
- Day-by-day timeline view of all activities
- Status tracking (Confirmed, Pending, Urgent)
- Interactive schedule with detailed event information
- Cost tracking and budget management

### 🌊 **Weather & Tide Intelligence**
- Current weather conditions and 6-day forecast
- UV index monitoring with sun protection recommendations
- Hourly tide schedule for beach activities
- Weather-based activity suggestions

### 🚗 **Travel Intelligence**
- Real-time flight status tracking (yours and John's)
- Travel time estimates from hotel to all locations
- Airport information and gate updates
- Route planning and navigation assistance

### 💆 **Spa Treatment Guide**
- Complete Ritz-Carlton spa menu with pricing
- Treatment descriptions and duration
- Direct booking integration
- Couples massage and birthday special options

### 💰 **Budget Tracker**
- Comprehensive spending breakdown by category
- Daily budget analysis with visual charts
- Confirmed vs. pending cost tracking
- Total trip budget management

### 🔒 **Privacy Protection**
- Password-protected sensitive information
- Demo mode for sharing without exposing personal details
- Secure masking of booking numbers, phone numbers, and flight details

## 🚀 Quick Start

### Local Development

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd 40th_Birthday_Trip_Assistant_DEPLOY
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:8501`
   - Default password: `hello`

### Streamlit Cloud Deployment

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Push all files from this folder to your repository

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Deploy!

3. **Configure Environment Variables**
   - In Streamlit Cloud dashboard, go to "Advanced settings"
   - Add environment variables from `env.example`
   - Redeploy if necessary

### Other Deployment Options

#### Heroku
```bash
# Add Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

#### Railway
```bash
# Railway will automatically detect Streamlit
railway login
railway init
railway up
```

#### Render
```bash
# Create render.yaml (see deployment guide)
# Connect GitHub repository to Render
# Deploy automatically
```

## 🎯 Trip Details

**Dates:** November 7-12, 2025  
**Location:** The Ritz-Carlton, Amelia Island  
**Occasion:** 40th Birthday Celebration  

### Key Activities
- ✈️ **Arrival:** November 7, 6:01 PM (AA2434)
- 🚤 **Backwater Cat Tour:** November 8, 3:30 PM
- 🎂 **Birthday Celebration:** November 9 (Spa + Dinner)
- 🏖️ **Beach & Relaxation:** November 10
- ✈️ **Departure:** November 12, 2:39 PM (AA5590)

### Urgent Bookings
- 🚤 Backwater Cat Adventures: (904) 753-7631
- 💆 Ritz-Carlton Spa: (904) 277-1100
- 🍽️ David's Restaurant: (904) 310-6049

## 🔧 Customization

### Changing the Password
1. Generate MD5 hash of your new password:
   ```bash
   echo -n "your_new_password" | md5sum
   ```
2. Update `TRIP_PASSWORD_HASH` in your environment variables

### Adding Your Own Data
- Edit the `load_trip_data()` function in `app.py`
- Replace sample data with your actual trip information
- Update flight numbers, dates, and booking details

### Styling Customization
- Modify CSS in the `load_deployment_css()` function
- Change colors by updating CSS variables
- Customize card styles and animations

## 📱 Mobile Optimization

The app is fully optimized for mobile devices with:
- Responsive design that works on all screen sizes
- Touch-friendly interface elements
- Fast loading and smooth animations
- Offline-capable design (with PWA features)

## 🔒 Security Features

- **Password Protection:** Sensitive information is protected
- **Data Masking:** Personal details are masked in demo mode
- **Secure Deployment:** Production-ready configuration
- **Environment Variables:** Sensitive data stored securely

## 🎨 Design Features

- **Modern UI:** Clean, professional design with smooth animations
- **Color Coded:** Status-based color coding for easy recognition
- **Interactive Elements:** Hover effects and responsive buttons
- **Visual Hierarchy:** Clear information organization
- **Brand Consistency:** Cohesive design throughout the app

## 📊 Technical Stack

- **Frontend:** Streamlit with custom CSS
- **Data Processing:** Pandas for data manipulation
- **Visualization:** Plotly for interactive charts
- **Deployment:** Streamlit Cloud, Heroku, Railway, or Render
- **Security:** Environment variables and data masking

## 🆘 Troubleshooting

### Common Issues

**App won't start:**
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version compatibility (3.8+)

**Password not working:**
- Default password is `hello`
- Check environment variable `TRIP_PASSWORD_HASH`

**Styling issues:**
- Clear browser cache
- Check CSS in `load_deployment_css()` function

**Deployment issues:**
- Verify all files are uploaded to repository
- Check environment variables in deployment platform
- Review deployment logs for specific errors

### Getting Help

1. Check the Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
2. Review deployment platform specific guides
3. Check browser console for JavaScript errors

## 📝 License

This project is created for personal use. Feel free to adapt it for your own trips and celebrations!

## 🎉 Enjoy Your Trip!

Have an amazing 40th birthday celebration at Amelia Island! This app will help you stay organized and make the most of every moment.

---

*Made with ❤️ for an unforgettable 40th birthday celebration*
