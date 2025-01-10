



// .NET Framework port by Kazuya Ujihara
// Copyright (C) 2016-2017  Kazuya Ujihara <ujihara.kazuya@gmail.com>

/* Copyright (C) 2005-2015  Egon Willighagen <egonw@users.sf.net>
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 * All we ask is that proper credit is given for our work, which includes
 * - but is not limited to - adding the above copyright notice to the beginning
 * of your source code files, and to any copyright notice that you may distribute
 * with programs based on this work.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT Any WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

using NCDK.Numerics;
using System;

namespace NCDK.Default
{
    /// <summary>
    /// Represents the idea of an atom as used in PDB files. It contains extra fields
    /// normally associated with atoms in such files.
    /// </summary>
    // @cdk.module data
    // @see  Atom
    public class PDBAtom 
        : Atom, ICloneable, IPDBAtom
    {
        public PDBAtom(ChemicalElement element)
            : this(element.Symbol)
        {
        }

        /// <summary>
        /// Constructs an IPDBAtom from a Element.
        /// </summary>
        /// <param name="element">IElement to copy information from</param>
        public PDBAtom(IElement element)
            : base(element)
        {
            InitValues();
        }

        /// <summary>
        /// Constructs an <see cref="IPDBAtom"/> from a string containing an element symbol.
        /// </summary>
        /// <param name="symbol">The string describing the element for the PDBAtom</param>
        public PDBAtom(string symbol)
            : base(symbol)
        {
            InitValues();
        }

        /// <summary>
        /// Constructs an <see cref="IPDBAtom"/> from an Element and a Vector3.
        /// </summary>
        /// <param name="symbol">The symbol of the atom</param>
        /// <param name="coordinate">The 3D coordinates of the atom</param>
        public PDBAtom(string symbol, Vector3 coordinate)
            : base(symbol, coordinate)
        {
            InitValues();
        }

        private void InitValues()
        {
            Record = null;
            TempFactor = -1.0;
            ResName = null;
            ICode = null;
            Occupancy = -1.0;
            Name = null;
            ChainID = null;
            AltLoc = null;
            SegID = null;
            Serial = 0;
            ResSeq = null;

            Oxt = false;
            HetAtom = false;

            base.ImplicitHydrogenCount = null;
            base.Charge = 0.0;
            base.FormalCharge = 0;
        }

        /// <summary>
        /// one entire line from the PDB entry file which describe the IPDBAtom.
        /// It consists of 80 columns.
        /// </summary>
        /// <returns>a string with all information</returns>
        public virtual string Record { get; set; }

        /// <summary>
        /// The Temperature factor of this atom.
        /// </summary>
        public double? TempFactor { get; set; }

        /// <summary>
        /// The Residue name of this atom.
        /// </summary>
        public string ResName { get; set; }

        /// <summary>
        /// The Code for insertion of residues of this atom.
        /// </summary>
        public string ICode { get; set; }

        /// <summary>
        /// The Atom name of this atom.
        /// </summary>

        public string Name { get; set; }

        /// <summary>
        /// The Chain identifier of this atom.
        /// </summary>
        public string ChainID { get; set; }

        /// <summary>
        /// The Alternate location indicator of this atom.
        /// </summary>
        public string AltLoc { get; set; }

        /// <summary>
        /// The Segment identifier, left-justified of this atom.
        /// </summary>
        public string SegID { get; set; }

        /// <summary>
        /// The Atom serial number of this atom.
        /// </summary>
        public int? Serial { get; set; }

        /// <summary>
        /// The Residue sequence number of this atom.
        /// </summary>
        public string ResSeq { get; set; }

        public bool Oxt { get; set; }

        public bool? HetAtom { get; set; }

        /// <summary>
        /// The Occupancy of this atom.
        /// </summary>

        public double? Occupancy { get; set; }
    }
}
namespace NCDK.Silent
{
    /// <summary>
    /// Represents the idea of an atom as used in PDB files. It contains extra fields
    /// normally associated with atoms in such files.
    /// </summary>
    // @cdk.module data
    // @see  Atom
    public class PDBAtom 
        : Atom, ICloneable, IPDBAtom
    {
        public PDBAtom(ChemicalElement element)
            : this(element.Symbol)
        {
        }

        /// <summary>
        /// Constructs an IPDBAtom from a Element.
        /// </summary>
        /// <param name="element">IElement to copy information from</param>
        public PDBAtom(IElement element)
            : base(element)
        {
            InitValues();
        }

        /// <summary>
        /// Constructs an <see cref="IPDBAtom"/> from a string containing an element symbol.
        /// </summary>
        /// <param name="symbol">The string describing the element for the PDBAtom</param>
        public PDBAtom(string symbol)
            : base(symbol)
        {
            InitValues();
        }

        /// <summary>
        /// Constructs an <see cref="IPDBAtom"/> from an Element and a Vector3.
        /// </summary>
        /// <param name="symbol">The symbol of the atom</param>
        /// <param name="coordinate">The 3D coordinates of the atom</param>
        public PDBAtom(string symbol, Vector3 coordinate)
            : base(symbol, coordinate)
        {
            InitValues();
        }

        private void InitValues()
        {
            Record = null;
            TempFactor = -1.0;
            ResName = null;
            ICode = null;
            Occupancy = -1.0;
            Name = null;
            ChainID = null;
            AltLoc = null;
            SegID = null;
            Serial = 0;
            ResSeq = null;

            Oxt = false;
            HetAtom = false;

            base.ImplicitHydrogenCount = null;
            base.Charge = 0.0;
            base.FormalCharge = 0;
        }

        /// <summary>
        /// one entire line from the PDB entry file which describe the IPDBAtom.
        /// It consists of 80 columns.
        /// </summary>
        /// <returns>a string with all information</returns>
        public virtual string Record { get; set; }

        /// <summary>
        /// The Temperature factor of this atom.
        /// </summary>
        public double? TempFactor { get; set; }

        /// <summary>
        /// The Residue name of this atom.
        /// </summary>
        public string ResName { get; set; }

        /// <summary>
        /// The Code for insertion of residues of this atom.
        /// </summary>
        public string ICode { get; set; }

        /// <summary>
        /// The Atom name of this atom.
        /// </summary>

        public string Name { get; set; }

        /// <summary>
        /// The Chain identifier of this atom.
        /// </summary>
        public string ChainID { get; set; }

        /// <summary>
        /// The Alternate location indicator of this atom.
        /// </summary>
        public string AltLoc { get; set; }

        /// <summary>
        /// The Segment identifier, left-justified of this atom.
        /// </summary>
        public string SegID { get; set; }

        /// <summary>
        /// The Atom serial number of this atom.
        /// </summary>
        public int? Serial { get; set; }

        /// <summary>
        /// The Residue sequence number of this atom.
        /// </summary>
        public string ResSeq { get; set; }

        public bool Oxt { get; set; }

        public bool? HetAtom { get; set; }

        /// <summary>
        /// The Occupancy of this atom.
        /// </summary>

        public double? Occupancy { get; set; }
    }
}
