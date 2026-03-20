import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { EnhancedHero } from './components/EnhancedHero';
import { RoomCard, Room, RoomPackage } from './components/RoomCard';
import { RoomDetails } from './components/RoomDetails';
import { Footer } from './components/Footer';
import { AdminPanel } from './components/AdminPanel';
import { AuthModal } from './components/AuthModal';
import { BookingModal } from './components/BookingModal';
import { Toaster, toast } from 'sonner';
import { motion, AnimatePresence } from 'motion/react';

import { MyBookings } from './components/MyBookings';
import { UserProfile } from './components/UserProfile';
import { api } from './services/api';

const INITIAL_ROOMS: Room[] = [];

export default function App() {
  const [view, setView] = useState<'customer' | 'staff'>('customer');
  const [customerView, setCustomerView] = useState<'home' | 'my-bookings' | 'profile'>('home');
  const [activeFilter, setActiveFilter] = useState('All Rooms');
  const [user, setUser] = useState<any>(null);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [selectedRoomForBooking, setSelectedRoomForBooking] = useState<Room | null>(null);
  const [selectedRoomForDetails, setSelectedRoomForDetails] = useState<Room | null>(null);
  const [isBookingOpen, setIsBookingOpen] = useState(false);
  const [userBookings, setUserBookings] = useState<any[]>([]);
  const [rooms, setRooms] = useState<Room[]>(INITIAL_ROOMS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRooms();
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const data = await api.checkAuth();
      if ((data as any).authenticated) {
        const userData = await api.getMe();
        setUser({
          ...userData,
          name: (userData as any).name || 'User',
          email: (userData as any).email
        });
      }
    } catch (error) {
      console.log('Not authenticated');
    }
  };

  const fetchRooms = async () => {
    try {
      const data = await api.getRooms({ status: 'available' });
      const mappedRooms = (data as any[]).map((room: any) => ({
        id: String(room.id),
        name: room.name,
        type: room.type,
        price: room.price,
        image: room.image,
        size: room.size,
        occupancy: room.occupancy,
        description: room.description,
        status: room.status,
        featured: room.featured,
        amenities: room.amenities?.map((a: any) => a.name) || [],
        packages: room.packages?.map((p: any) => ({
          id: String(p.id),
          name: p.name,
          description: p.description,
          priceMultiplier: p.price_multiplier
        })) || []
      }));
      setRooms(mappedRooms);
    } catch (error) {
      console.error('Failed to fetch rooms:', error);
      toast.error('Failed to load rooms from database');
    } finally {
      setLoading(false);
    }
  };

  const filteredRooms = rooms.filter(room => 
    (activeFilter === 'All Rooms' || room.type === activeFilter) && 
    room.status === 'available'
  );

  const featuredRoom = rooms.find(room => room.featured && room.status === 'available') || null;

  const handleBookingConfirm = async (details: any) => {
    try {
      const packageId = details.package?.id ? parseInt(details.package.id) : undefined;
      const booking = await api.createBooking({
        room_id: parseInt(details.room.id),
        check_in: new Date().toISOString(),
        check_out: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(),
        package_id: (!isNaN(packageId as number) && packageId !== undefined) ? packageId : undefined
      });
      
      const newBooking = {
        id: (booking as any).id || `BK-${Math.floor(Math.random() * 9000) + 1000}`,
        roomName: details.room.name,
        roomImage: details.room.image,
        checkIn: (booking as any).check_in, 
        checkOut: (booking as any).check_out,
        total: (booking as any).total_price,
        status: (booking as any).status || 'confirmed',
        package: details.package?.name || 'Room Only'
      };
      
      setUserBookings([newBooking, ...userBookings]);
      toast.success('Booking Successful!', {
        description: `Your reservation for ${details.room.name} has been confirmed.`,
      });
    } catch (error) {
      console.error('Booking failed:', error);
      toast.error('Failed to create booking');
      const newBooking = {
        id: `BK-${Math.floor(Math.random() * 9000) + 1000}`,
        roomName: details.room.name,
        roomImage: details.room.image,
        checkIn: '2026-02-12', 
        checkOut: '2026-02-14',
        total: details.total,
        status: 'confirmed',
        package: details.package.name
      };
      setUserBookings([newBooking, ...userBookings]);
    }
    setIsBookingOpen(false);
    setSelectedRoomForBooking(null);
    setCustomerView('my-bookings');
  };

  const handleSearch = async (params: any) => {
    const children = params.children || 0;
    
    try {
      const data = await api.getRooms({ 
        status: 'available',
        children: children
      });
      const mappedRooms = (data as any[]).map((room: any) => ({
        id: String(room.id),
        name: room.name,
        type: room.type,
        price: room.price,
        image: room.image,
        size: room.size,
        occupancy: room.occupancy,
        description: room.description,
        status: room.status,
        featured: room.featured,
        amenities: room.amenities?.map((a: any) => a.name) || [],
        packages: room.packages?.map((p: any) => ({
          id: String(p.id),
          name: p.name,
          description: p.description,
          priceMultiplier: p.price_multiplier
        })) || []
      }));
      setRooms(mappedRooms);
      setActiveFilter('All Rooms');
      
      const element = document.getElementById('rooms-section');
      element?.scrollIntoView({ behavior: 'smooth' });
      toast.success(`Found ${mappedRooms.length} rooms!`);
    } catch (error) {
      console.error('Search failed:', error);
      toast.error('Error searching for rooms');
    }
  };

  const handleBookNow = (room: Room) => {
    if (!user) {
      toast.info('Please log in to book a room');
      setIsAuthOpen(true);
    } else {
      setSelectedRoomForBooking(room);
      setIsBookingOpen(true);
    }
  };

  const handleViewDetails = (room: Room) => {
    setSelectedRoomForDetails(room);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCancelBooking = async (bookingId: string) => {
    try {
      await api.cancelBooking(bookingId);
      setUserBookings(prev => prev.map(b => b.id === bookingId ? { ...b, status: 'cancelled' } : b));
      toast.success('Booking cancelled successfully');
    } catch (error) {
      console.error('Cancel booking failed:', error);
      setUserBookings(prev => prev.map(b => b.id === bookingId ? { ...b, status: 'cancelled' } : b));
      toast.info('Booking marked as cancelled');
    }
  };

  const handleUpdateProfile = (userData: any) => {
    setUser({ ...user, ...userData });
  };

  const handleUpdateRoom = (roomId: string, updates: Partial<Room>) => {
    setRooms(prev => prev.map(room => 
      room.id === roomId ? { ...room, ...updates } : room
    ));
  };

  const handleAddPackage = (roomId: string, packageData: RoomPackage) => {
    setRooms(prev => prev.map(room => 
      room.id === roomId 
        ? { ...room, packages: [...(room.packages || []), packageData] }
        : room
    ));
  };

  const handleRemovePackage = (roomId: string, packageId: string) => {
    setRooms(prev => prev.map(room => 
      room.id === roomId 
        ? { ...room, packages: room.packages?.filter(pkg => pkg.id !== packageId) }
        : room
    ));
  };

  const handleViewFeatured = () => {
    if (featuredRoom) {
      setSelectedRoomForDetails(featuredRoom);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans selection:bg-primary/20 selection:text-primary">
      <Toaster position="top-right" expand={false} richColors />
      
      <Navbar 
        user={user} 
        onAuthClick={() => setIsAuthOpen(true)} 
        onLogout={async () => {
          try {
            await api.logout();
          } catch (e) {}
          setUser(null);
          setView('customer');
          setCustomerView('home');
          toast.info('Logged out successfully');
        }}
        onProfileClick={() => {
          setView('customer');
          setCustomerView('profile');
        }}
        view={view}
        setView={(v) => {
          setView(v);
          setSelectedRoomForDetails(null);
        }}
        customerView={customerView}
        setCustomerView={setCustomerView}
      />

      <main className="flex-grow">
        <AnimatePresence mode="wait">
          {view === 'customer' ? (
            <motion.div
              key={selectedRoomForDetails ? 'details' : customerView}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
            >
              {selectedRoomForDetails ? (
                <RoomDetails 
                  room={selectedRoomForDetails} 
                  onBack={() => setSelectedRoomForDetails(null)} 
                  onBookNow={handleBookNow}
                />
              ) : customerView === 'my-bookings' ? (
                <MyBookings 
                  bookings={userBookings} 
                  onBack={() => setCustomerView('home')}
                  onCancelBooking={handleCancelBooking}
                />
              ) : customerView === 'profile' ? (
                <UserProfile 
                  user={user}
                  onBack={() => setCustomerView('home')}
                  onUpdate={handleUpdateProfile}
                />
              ) : (
                <>
                  <EnhancedHero 
                    onBookNow={() => {
                      const element = document.getElementById('rooms-section');
                      element?.scrollIntoView({ behavior: 'smooth' });
                    }} 
                    onSearch={handleSearch}
                    featuredRoom={featuredRoom}
                    onViewFeatured={handleViewFeatured}
                  />
                  
                  <section id="rooms-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
                    <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4">
                      <div>
                        <h2 className="text-4xl font-bold mb-4">Our Curated Rooms</h2>
                        <p className="text-muted-foreground max-w-xl">
                          Each room is meticulously designed to provide a haven of tranquility amidst the vibrant pulse of Hong Kong.
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {['All Rooms', 'Luxury', 'Suite', 'Business', 'Family'].map((filter) => (
                          <button 
                            key={filter} 
                            onClick={() => setActiveFilter(filter)}
                            className={`px-6 py-2 rounded-full border text-sm font-bold transition-all cursor-pointer ${
                              activeFilter === filter 
                                ? 'bg-primary text-primary-foreground border-primary shadow-md' 
                                : 'border-border text-muted-foreground hover:bg-muted'
                            }`}
                          >
                            {filter}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                      {loading ? (
                        <div className="col-span-full py-12 text-center text-muted-foreground">
                          <div className="animate-pulse">Loading rooms from database...</div>
                        </div>
                      ) : filteredRooms.length > 0 ? (
                        filteredRooms.map((room) => (
                          <RoomCard 
                            key={room.id} 
                            room={room} 
                            onViewDetails={handleViewDetails}
                            onBookNow={handleBookNow}
                          />
                        ))
                      ) : (
                        <div className="col-span-full py-12 text-center text-muted-foreground">
                          No rooms found matching this category.
                        </div>
                      )}
                    </div>
                  </section>

                  {/* Amenities Section */}
                  <section className="bg-muted/30 py-24">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                      <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold mb-4">World-Class Facilities</h2>
                        <p className="text-muted-foreground max-w-2xl mx-auto">
                          Beyond your room, explore a world of dining, relaxation, and wellness.
                        </p>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="group relative h-80 rounded-2xl overflow-hidden shadow-lg cursor-pointer">
                          <img src="https://images.unsplash.com/photo-1769638913569-40fc740b44f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxob3RlbCUyMGJyZWFrZmFzdCUyMGJ1ZmZldCUyMHNlbGVjdGlvbiUyMGZyZXNoJTIwZm9vZHxlbnwxfHx8fDE3NzA4NTMyOTh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" alt="Dining" />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent flex flex-col justify-end p-8 text-white">
                            <h3 className="text-xl font-bold mb-2">Exquisite Dining</h3>
                            <p className="text-sm opacity-80">Award-winning Cantonese and international cuisine.</p>
                          </div>
                        </div>
                        <div className="group relative h-80 rounded-2xl overflow-hidden shadow-lg cursor-pointer">
                          <img src="https://images.unsplash.com/photo-1761049862641-16616dea7b32?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBob3RlbCUyMHNwYSUyMHdlbGxuZXNzJTIwY2VudGVyJTIwcG9vbHxlbnwxfHx8fDE3NzA4NTMyOTh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" alt="Spa" />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent flex flex-col justify-end p-8 text-white">
                            <h3 className="text-xl font-bold mb-2">Wellness & Spa</h3>
                            <p className="text-sm opacity-80">Rejuvenate your senses with our holistic treatments.</p>
                          </div>
                        </div>
                        <div className="group relative h-80 rounded-2xl overflow-hidden shadow-lg cursor-pointer">
                          <img src="https://images.unsplash.com/photo-1742844552193-2fd3425cd26d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBob3RlbCUyMGxvYmJ5JTIwaW50ZXJpb3IlMjBoaWdoJTIwcmVzb2x1dGlvbnxlbnwxfHx8fDE3NzA4NTMyOTh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" alt="Lobby" />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent flex flex-col justify-end p-8 text-white">
                            <h3 className="text-xl font-bold mb-2">Luxury Lounge</h3>
                            <p className="text-sm opacity-80">Relax in our elegantly designed guest spaces.</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </section>
                </>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="staff"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <AdminPanel 
                rooms={rooms}
                onUpdateRoom={handleUpdateRoom}
                onAddPackage={handleAddPackage}
                onRemovePackage={handleRemovePackage}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <Footer />

      <AuthModal 
        isOpen={isAuthOpen} 
        onClose={() => setIsAuthOpen(false)} 
        onSuccess={(userData) => {
          setUser(userData);
          toast.success(`Welcome back, ${userData.name}!`);
          if (userData.role === 'staff') {
            setView('staff');
          }
        }} 
      />

      <BookingModal 
        room={selectedRoomForBooking} 
        isOpen={isBookingOpen} 
        onClose={() => {
          setIsBookingOpen(false);
          setSelectedRoomForBooking(null);
        }} 
        onConfirm={handleBookingConfirm}
        user={user}
      />
    </div>
  );
}
