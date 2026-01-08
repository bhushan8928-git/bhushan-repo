import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { MapPin, Star, Clock, Calendar, DollarSign, ArrowLeft } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { axiosInstance } from '../App';
import { toast } from 'sonner';

const PlaceDetail = () => {
  const { placeId } = useParams();
  const [place, setPlace] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPlace = async () => {
      try {
        const response = await axiosInstance.get(`/places/${placeId}`);
        setPlace(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching place:', error);
        toast.error('Failed to load place details');
        setLoading(false);
      }
    };
    fetchPlace();
  }, [placeId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-2xl font-heading text-primary">Loading...</div>
      </div>
    );
  }

  if (!place) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-2xl font-heading text-muted-foreground">Place not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Image */}
      <motion.section 
        className="relative h-[60vh] w-full overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <img
          src={place.image}
          alt={place.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        
        <Link to="/" data-testid="back-button">
          <motion.button
            className="absolute top-8 left-8 bg-white/10 backdrop-blur-md text-white px-6 py-3 rounded-full flex items-center gap-2 hover:bg-white/20 transition-colors font-body"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <ArrowLeft size={20} />
            Back
          </motion.button>
        </Link>

        <div className="absolute top-8 right-8 bg-secondary text-secondary-foreground px-6 py-3 rounded-full font-body text-lg font-semibold">
          {place.price}
        </div>
      </motion.section>

      {/* Place Details */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {/* Main Content */}
            <div className="lg:col-span-2">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <h1 className="text-5xl md:text-6xl font-heading font-bold tracking-tight mb-4">
                  {place.name}
                </h1>
                
                <div className="flex items-center gap-6 mb-8">
                  <div className="flex items-center gap-2">
                    <Star size={24} className="fill-secondary text-secondary" />
                    <span className="text-2xl font-heading font-semibold">{place.rating}</span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <MapPin size={20} />
                    <span className="font-body">Lat: {place.location.lat}, Lng: {place.location.lng}</span>
                  </div>
                </div>

                <p className="text-lg font-body leading-relaxed text-foreground mb-12">
                  {place.description}
                </p>

                {/* Map Section */}
                <div className="bg-muted rounded-lg p-12 mb-12">
                  <h2 className="text-3xl font-heading font-semibold mb-6">Location</h2>
                  <div className="aspect-video bg-accent rounded-lg flex items-center justify-center">
                    <iframe
                      title="Location Map"
                      width="100%"
                      height="100%"
                      style={{ border: 0, borderRadius: '0.5rem' }}
                      loading="lazy"
                      allowFullScreen
                      src={`https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q=${place.location.lat},${place.location.lng}&zoom=12`}
                    />
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="sticky top-8"
              >
                <div className="bg-card rounded-lg shadow-lg p-8 space-y-6">
                  <h3 className="text-2xl font-heading font-semibold mb-6">Trip Details</h3>
                  
                  <div className="space-y-4">
                    <div className="flex items-start gap-4 p-4 bg-muted rounded-lg">
                      <DollarSign className="text-secondary mt-1" size={24} />
                      <div>
                        <div className="font-body font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-1">
                          Price Range
                        </div>
                        <div className="text-xl font-heading font-semibold">{place.price}</div>
                      </div>
                    </div>

                    <div className="flex items-start gap-4 p-4 bg-muted rounded-lg">
                      <Calendar className="text-secondary mt-1" size={24} />
                      <div>
                        <div className="font-body font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-1">
                          Best Time to Visit
                        </div>
                        <div className="text-lg font-body">{place.best_time}</div>
                      </div>
                    </div>

                    <div className="flex items-start gap-4 p-4 bg-muted rounded-lg">
                      <Clock className="text-secondary mt-1" size={24} />
                      <div>
                        <div className="font-body font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-1">
                          Recommended Duration
                        </div>
                        <div className="text-lg font-body">{place.duration}</div>
                      </div>
                    </div>

                    <div className="flex items-start gap-4 p-4 bg-muted rounded-lg">
                      <Star className="text-secondary mt-1 fill-secondary" size={24} />
                      <div>
                        <div className="font-body font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-1">
                          Traveler Rating
                        </div>
                        <div className="text-lg font-body">{place.rating} / 5.0</div>
                      </div>
                    </div>
                  </div>

                  <button 
                    className="w-full bg-primary text-primary-foreground py-4 rounded-full font-body font-semibold text-lg hover:bg-primary/90 transition-colors mt-8"
                    data-testid="book-trip-button"
                    onClick={() => toast.success('Booking feature coming soon!')}
                  >
                    Book This Trip
                  </button>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default PlaceDetail;