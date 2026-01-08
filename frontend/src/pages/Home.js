import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Star, ArrowRight, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import { axiosInstance } from '../App';
import { toast } from 'sonner';

const Home = () => {
  const [countries, setCountries] = useState([]);
  const [allPlaces, setAllPlaces] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [countriesRes, placesRes] = await Promise.all([
          axiosInstance.get('/countries'),
          axiosInstance.get('/places')
        ]);
        setCountries(countriesRes.data);
        setAllPlaces(placesRes.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        toast.error('Failed to load destinations');
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const trendingPlaces = allPlaces.slice(0, 6);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-2xl font-heading text-primary">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <motion.section 
        className="relative h-screen w-full flex items-center justify-center overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1920')`
          }}
        />
        <div className="absolute inset-0 hero-gradient" />
        
        <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
          <motion.h1 
            className="text-6xl md:text-8xl font-heading font-bold tracking-tighter leading-none text-white mb-8"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            Dream. Plan. Go.
          </motion.h1>
          
          <motion.p 
            className="text-lg md:text-xl text-white/90 mb-12 font-body leading-relaxed"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            Discover handpicked destinations across the globe
          </motion.p>

          <motion.div 
            className="max-w-2xl mx-auto"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <div className="relative search-blur bg-white/10 rounded-full p-2 border border-white/20">
              <div className="flex items-center gap-4 px-6">
                <Search className="text-white/70" size={24} />
                <input
                  type="text"
                  placeholder="Search destinations..."
                  data-testid="hero-search-input"
                  className="flex-1 bg-transparent border-none outline-none text-white placeholder:text-white/60 text-lg py-4 font-body"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
          </motion.div>
        </div>
      </motion.section>

      {/* Countries Section */}
      <section className="py-20 md:py-32 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-6xl font-heading font-semibold tracking-tight mb-4">
              Explore Countries
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground mb-12 font-body leading-relaxed">
              Curated destinations waiting for your adventure
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
            {countries.map((country, index) => (
              <motion.div
                key={country.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
              >
                <Link to={`/country/${country.id}`} data-testid={`country-card-${country.id}`}>
                  <div className="country-card group relative h-[500px] w-full overflow-hidden rounded-lg cursor-pointer">
                    <img
                      src={country.hero_image}
                      alt={country.name}
                      className="country-card-image absolute inset-0 w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 card-overlay" />
                    
                    <div className="absolute bottom-0 left-0 right-0 p-8 text-white">
                      <h3 className="text-4xl md:text-5xl font-heading font-semibold mb-2">
                        {country.name}
                      </h3>
                      <p className="text-white/80 mb-4 font-body">
                        {country.description}
                      </p>
                      <div className="flex items-center gap-2 text-white/90 group-hover:gap-4 transition-all">
                        <span className="font-body uppercase text-sm tracking-widest">Explore</span>
                        <ArrowRight size={20} />
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Trending Places */}
      <section className="py-20 md:py-32 px-4 bg-muted">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-6xl font-heading font-semibold tracking-tight mb-4">
              Trending Destinations
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground mb-12 font-body leading-relaxed">
              Most popular places travelers are exploring
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {trendingPlaces.map((place, index) => (
              <motion.div
                key={place.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
              >
                <Link to={`/place/${place.id}`} data-testid={`place-card-${place.id}`}>
                  <div className="place-card-hover bg-card rounded-lg overflow-hidden shadow-sm">
                    <div className="relative aspect-[4/3]">
                      <img
                        src={place.image}
                        alt={place.name}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute top-4 right-4 bg-secondary text-secondary-foreground px-4 py-2 rounded-full font-body text-sm font-semibold">
                        {place.price}
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <h3 className="text-2xl md:text-3xl font-heading font-medium mb-2">
                        {place.name}
                      </h3>
                      <div className="flex items-center gap-2 text-muted-foreground mb-3">
                        <MapPin size={16} />
                        <span className="font-body text-sm">{place.duration}</span>
                        <div className="flex items-center gap-1 ml-auto">
                          <Star size={16} className="fill-secondary text-secondary" />
                          <span className="font-body text-sm font-semibold">{place.rating}</span>
                        </div>
                      </div>
                      <p className="text-muted-foreground font-body text-sm leading-relaxed line-clamp-2">
                        {place.description}
                      </p>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-primary text-primary-foreground py-12 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h3 className="text-3xl font-heading font-semibold mb-4">Ready for Adventure?</h3>
          <p className="text-primary-foreground/80 font-body mb-8">
            Start planning your dream vacation today
          </p>
          <div className="text-primary-foreground/60 font-body text-sm">
            © 2025 Travel Recommendations. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;