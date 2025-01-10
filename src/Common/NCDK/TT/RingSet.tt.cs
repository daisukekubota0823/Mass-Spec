



// .NET Framework port by Kazuya Ujihara
// Copyright (C) 2016-2017  Kazuya Ujihara <ujihara.kazuya@gmail.com>

/* Copyright (C) 1997-2007  Christoph Steinbeck <steinbeck@users.sf.net>
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

using System;
using System.Collections.Generic;
using System.Linq;

namespace NCDK.Default
{
    /// <summary>
    /// Maintains a set of Ring objects.
    /// </summary>
    // @cdk.keyword ring, set of
    [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Naming", "CA1710:IdentifiersShouldHaveCorrectSuffix", Justification = "Ignored")]
    public class RingSet
        : ChemObjectSet<IRing>, IRingSet, ICloneable
    {
        /// <summary>
        /// The constructor.
        /// </summary>
        public RingSet()
        {
        }

        /// <summary>
        /// Returns a vector of all rings that this atom is part of.
        /// </summary>
        /// <param name="atom">The atom to be checked</param>
        /// <returns>A vector of all rings that this bond is part of</returns>
        public IEnumerable<IRing> GetRings(IAtom atom) => this.Where(n => n.Contains(atom));

        /// <summary>
        /// Returns a vector of all rings that this bond is part of.
        /// </summary>
        /// <param name="bond">The bond to be checked</param>
        /// <returns>A vector of all rings that this bond is part of</returns>
        public IEnumerable<IRing> GetRings(IBond bond) => this.Where(n => n.Contains(bond));

        /// <summary>
        /// Returns all the rings in the RingSet that share one or more atoms with a given ring.
        /// </summary>
        /// <param name="ring">A ring with which all return rings must share one or more atoms</param>
        /// <returns>All the rings that share one or more atoms with a given ring.</returns>
        public IEnumerable<IRing> GetConnectedRings(IRing ring)
        {
            IRingSet connectedRings = ring.Builder.NewRingSet();
            foreach (var atom in ring.Atoms)
                foreach (var tempRing in this)
                    if (tempRing != ring
                      && !connectedRings.Contains(tempRing)
                      && tempRing.Contains(atom))
                    {
                        connectedRings.Add(tempRing);
                    }
            return connectedRings;
        }

        /// <summary>
        /// Adds all rings of another RingSet if they are not already part of this ring set.
        /// 
        /// If you want to add a single ring to the set use <see cref="Add(IRingSet)"/> 
        /// </summary>
        /// <param name="ringSet">the ring set to be united with this one.</param>
        public void Add(IRingSet ringSet)
        {
            foreach (var ring in ringSet)
                if (!Contains(ring))
                    Add(ring);
        }

        /// <summary>
        /// True, if at least one of the rings in the ringset contains the given atom.
        /// </summary>
        /// <param name="atom">Atom to check</param>
        /// <returns>true, if the ringset contains the atom</returns>
        public bool Contains(IAtom atom)
            => this.Any(n => n.Contains(atom));
    }
}
namespace NCDK.Silent
{
    /// <summary>
    /// Maintains a set of Ring objects.
    /// </summary>
    // @cdk.keyword ring, set of
    [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Naming", "CA1710:IdentifiersShouldHaveCorrectSuffix", Justification = "Ignored")]
    public class RingSet
        : ChemObjectSet<IRing>, IRingSet, ICloneable
    {
        /// <summary>
        /// The constructor.
        /// </summary>
        public RingSet()
        {
        }

        /// <summary>
        /// Returns a vector of all rings that this atom is part of.
        /// </summary>
        /// <param name="atom">The atom to be checked</param>
        /// <returns>A vector of all rings that this bond is part of</returns>
        public IEnumerable<IRing> GetRings(IAtom atom) => this.Where(n => n.Contains(atom));

        /// <summary>
        /// Returns a vector of all rings that this bond is part of.
        /// </summary>
        /// <param name="bond">The bond to be checked</param>
        /// <returns>A vector of all rings that this bond is part of</returns>
        public IEnumerable<IRing> GetRings(IBond bond) => this.Where(n => n.Contains(bond));

        /// <summary>
        /// Returns all the rings in the RingSet that share one or more atoms with a given ring.
        /// </summary>
        /// <param name="ring">A ring with which all return rings must share one or more atoms</param>
        /// <returns>All the rings that share one or more atoms with a given ring.</returns>
        public IEnumerable<IRing> GetConnectedRings(IRing ring)
        {
            IRingSet connectedRings = ring.Builder.NewRingSet();
            foreach (var atom in ring.Atoms)
                foreach (var tempRing in this)
                    if (tempRing != ring
                      && !connectedRings.Contains(tempRing)
                      && tempRing.Contains(atom))
                    {
                        connectedRings.Add(tempRing);
                    }
            return connectedRings;
        }

        /// <summary>
        /// Adds all rings of another RingSet if they are not already part of this ring set.
        /// 
        /// If you want to add a single ring to the set use <see cref="Add(IRingSet)"/> 
        /// </summary>
        /// <param name="ringSet">the ring set to be united with this one.</param>
        public void Add(IRingSet ringSet)
        {
            foreach (var ring in ringSet)
                if (!Contains(ring))
                    Add(ring);
        }

        /// <summary>
        /// True, if at least one of the rings in the ringset contains the given atom.
        /// </summary>
        /// <param name="atom">Atom to check</param>
        /// <returns>true, if the ringset contains the atom</returns>
        public bool Contains(IAtom atom)
            => this.Any(n => n.Contains(atom));
    }
}
