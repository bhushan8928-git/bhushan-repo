import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Star, Clock, Calendar, ArrowLeft } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { axiosInstance } from '../App';
import { toast } from 'sonner';

const CountryDetail = () => {
  const { countryId } = useParams();
  const [country, setCountry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCountry = async () => {
      try {
        const response = await axiosInstance.get(`/countries/${countryId}`);
        setCountry(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching country:', error);
        toast.error('Failed to load country details');
        setLoading(false);
      }
    };
    fetchCountry();
  }, [countryId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-2xl font-heading text-primary">Loading...</div>
      </div>
    );
  }

  if (!country) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-2xl font-heading text-muted-foreground">Country not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <motion.section 
        className="relative h-[70vh] w-full flex items-center justify-center overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: `url('${country.hero_image}')`
          }}
        />
        <div className="absolute inset-0 hero-gradient" />
        
        <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
          <Link to="/" data-testid="back-to-home-link">
            <motion.button
              className="absolute top-8 left-8 bg-white/10 backdrop-blur-md text-white px-6 py-3 rounded-full flex items-center gap-2 hover:bg-white/20 transition-colors font-body"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <ArrowLeft size={20} />
              Back
            </motion.button>
          </Link>

          <motion.h1 
            className="text-6xl md:text-8xl font-heading font-bold tracking-tighter leading-none text-white mb-6"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            {country.name}
          </motion.h1>
          
          <motion.p 
            className="text-lg md:text-xl text-white/90 font-body leading-relaxed max-w-2xl mx-auto"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            {country.description}
          </motion.p>
        </div>
      </motion.section>

      {/* Places Grid */}
      <section className="py-20 md:py-32 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-6xl font-heading font-semibold tracking-tight mb-4">
              Top Destinations
            </h2>
            <p className="text-lg md:text-xl text-muted-foreground mb-12 font-body leading-relaxed">
              {country.places.length} must-visit places in {country.name}
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {country.places.map((place, index) => (
              <motion.div
                key={place.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
              >
                <Link to={`/place/${place.id}`} data-testid={`place-detail-card-${place.id}`}>
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
                      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full flex items-center gap-1">
                        <Star size={16} className="fill-secondary text-secondary" />
                        <span className="font-body text-sm font-semibold">{place.rating}</span>
                      </div>
                    </div>
                    
                    <div className="p-6">
                      <h3 className="text-2xl md:text-3xl font-heading font-medium mb-3">
                        {place.name}
                      </h3>
                      
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Calendar size={16} />
                          <span className="font-body text-sm">{place.best_time}</span>
                        </div>
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Clock size={16} />
                          <span className="font-body text-sm">{place.duration}</span>
                        </div>
                      </div>
                      
                      <p className="text-muted-foreground font-body text-sm leading-relaxed line-clamp-3">
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

      {/* CTA Section */}
      <section className="py-20 px-4 bg-primary text-primary-foreground">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-4xl md:text-5xl font-heading font-semibold mb-6">
            Ready to Explore {country.name}?
          </h3>
          <p className="text-lg text-primary-foreground/80 font-body mb-8">
            Plan your perfect trip with personalized recommendations
          </p>
        </div>
      </section>
    </div>
  );
};

export default CountryDetail;